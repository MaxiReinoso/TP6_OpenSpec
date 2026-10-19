import pytest
from fastapi.testclient import TestClient

from app.main import build_app
from app.models import Clase, EstadoMembresia, Socio
from app.service import ReservaService
from app.store import Almacen


@pytest.fixture
def almacen() -> Almacen:
    a = Almacen()
    a.agregar_socio(
        Socio(id="s1", nombre="Ana", estado_membresia=EstadoMembresia.activa)
    )
    a.agregar_socio(
        Socio(id="s2", nombre="Beto", estado_membresia=EstadoMembresia.activa)
    )
    a.agregar_clase(
        Clase(id="yoga", nombre="Yoga", horario="2026-10-19T18:00:00+00:00", cupo_maximo=1, instructor="Lucía")
    )
    a.agregar_clase(
        Clase(id="spinning", nombre="Spinning", horario="2026-10-19T18:00:00+00:00", cupo_maximo=5, instructor="Marcos")
    )
    a.agregar_clase(
        Clase(id="pilates", nombre="Pilates", horario="2026-10-19T20:00:00+00:00", cupo_maximo=1, instructor="Sara")
    )
    return a


@pytest.fixture
def client(almacen: Almacen) -> TestClient:
    return TestClient(build_app(ReservaService(almacen)))


def test_modelo_persiste_y_recupera_reserva(client, almacen):
    respuesta = client.post("/reservas", json={"socio_id": "s1", "clase_id": "spinning"})
    assert respuesta.status_code == 201

    reservas = almacen.reservas_de_socio("s1")
    assert len(reservas) == 1
    assert reservas[0].clase_id == "spinning"
    assert reservas[0].estado.value == "activa"

    clase = almacen.obtener_clase("spinning")
    assert clase is not None
    assert clase.cupo_maximo == 5


def test_reserva_con_cupo_disponible_descuenta_cupo(client, almacen):
    respuesta = client.post("/reservas", json={"socio_id": "s1", "clase_id": "spinning"})
    assert respuesta.status_code == 201
    assert respuesta.json()["estado"] == "activa"
    assert almacen.cupos_restantes("spinning") == 4

    listado = {c["id"]: c for c in client.get("/clases").json()}
    assert listado["spinning"]["cupos_restantes"] == 4


def test_clase_completa_rechaza_sin_descontar_cupo(client, almacen):
    primera = client.post("/reservas", json={"socio_id": "s1", "clase_id": "yoga"})
    assert primera.status_code == 201
    assert almacen.cupos_restantes("yoga") == 0

    rechazo = client.post("/reservas", json={"socio_id": "s2", "clase_id": "yoga"})
    assert rechazo.status_code == 409
    assert rechazo.json()["detail"] == "Clase completa"
    assert almacen.cupos_restantes("yoga") == 0


def test_reserva_duplicada_en_mismo_horario_se_rechaza(client, almacen):
    assert client.post("/reservas", json={"socio_id": "s1", "clase_id": "yoga"}).status_code == 201

    duplicada = client.post(
        "/reservas", json={"socio_id": "s1", "clase_id": "spinning"}
    )
    assert duplicada.status_code == 409
    assert almacen.cupos_restantes("spinning") == 5


def test_mismo_socio_otro_horario_se_permite(client):
    assert client.post("/reservas", json={"socio_id": "s1", "clase_id": "yoga"}).status_code == 201

    otra = client.post("/reservas", json={"socio_id": "s1", "clase_id": "pilates"})
    assert otra.status_code == 201


def test_listado_de_clases_expone_cupos_restantes(client):
    listado = {c["id"]: c for c in client.get("/clases").json()}
    assert listado["yoga"]["cupos_restantes"] == 1
    assert listado["spinning"]["cupos_restantes"] == 5

    client.post("/reservas", json={"socio_id": "s2", "clase_id": "yoga"})

    listado = {c["id"]: c for c in client.get("/clases").json()}
    assert listado["yoga"]["cupos_restantes"] == 0

from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import build_app
from app.models import Clase, Socio
from app.service import ReservaService
from app.store import Almacen

BASE = datetime(2026, 10, 19, 18, 0, tzinfo=timezone.utc)
DIAS = [timedelta(0), timedelta(days=1), timedelta(days=2), timedelta(days=10)]


@pytest.fixture
def almacen() -> Almacen:
    a = Almacen()
    a.agregar_socio(Socio(id="s1", nombre="Ana"))
    a.agregar_socio(Socio(id="s2", nombre="Beto"))
    for i, delta in enumerate(DIAS, start=1):
        a.agregar_clase(
            Clase(
                id=f"c{i}",
                nombre=f"Clase {i}",
                horario=(BASE + delta).isoformat(),
                cupo_maximo=1,
                instructor="Profe",
            )
        )
    return a


@pytest.fixture
def servicio(almacen: Almacen) -> ReservaService:
    return ReservaService(almacen)


@pytest.fixture
def reloj() -> dict:
    return {"ahora": BASE - timedelta(days=1, hours=5)}


@pytest.fixture
def client(servicio: ReservaService, reloj: dict) -> TestClient:
    return TestClient(build_app(servicio, ahora_provider=lambda: reloj["ahora"]))


def _acumular_ausencias(client: TestClient, reloj: dict, cantidad: int = 3) -> None:
    for i in range(1, cantidad + 1):
        fecha = BASE + DIAS[i - 1]
        reloj["ahora"] = fecha - timedelta(hours=5)
        reserva = client.post(
            "/reservas", json={"socio_id": "s1", "clase_id": f"c{i}"}
        ).json()
        reloj["ahora"] = fecha - timedelta(hours=1)
        client.post(f"/reservas/{reserva['id']}/cancel")


def test_cancelar_a_tiempo_libera_cupo(client, almacen, reloj):
    reloj["ahora"] = BASE + timedelta(days=1) - timedelta(hours=5)
    reserva = client.post(
        "/reservas", json={"socio_id": "s2", "clase_id": "c2"}
    ).json()

    reloj["ahora"] = BASE + timedelta(days=1) - timedelta(hours=3)
    respuesta = client.post(f"/reservas/{reserva['id']}/cancel")

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "cancelada"
    assert almacen.cupos_restantes("c2") == 1


def test_cancelar_tardi_marca_ausencia_sin_liberar_cupo(client, almacen, reloj):
    reloj["ahora"] = BASE - timedelta(hours=5)
    reserva = client.post(
        "/reservas", json={"socio_id": "s1", "clase_id": "c1"}
    ).json()

    reloj["ahora"] = BASE - timedelta(hours=1)
    respuesta = client.post(f"/reservas/{reserva['id']}/cancel")

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "ausente"
    assert almacen.cupos_restantes("c1") == 0


def test_ausencias_se_calculan_en_los_ultimos_30_dias(client, servicio, reloj):
    _acumular_ausencias(client, reloj)

    reloj["ahora"] = BASE + timedelta(days=2)
    assert len(servicio.ausencias("s1", ahora=reloj["ahora"])) == 3


def test_tres_ausencias_bloquean_nuevas_reservas_7_dias(client, reloj):
    _acumular_ausencias(client, reloj)

    reloj["ahora"] = BASE + timedelta(days=3)
    respuesta = client.post(
        "/reservas", json={"socio_id": "s1", "clase_id": "c4"}
    )
    assert respuesta.status_code == 403
    assert "bloqueadas" in respuesta.json()["detail"].lower()


def test_bloqueo_termina_tras_7_dias(client, reloj):
    _acumular_ausencias(client, reloj)

    ultima_ausencia = BASE + timedelta(days=2) - timedelta(hours=5)
    reloj["ahora"] = ultima_ausencia + timedelta(days=8)
    respuesta = client.post(
        "/reservas", json={"socio_id": "s1", "clase_id": "c4"}
    )
    assert respuesta.status_code == 201

from __future__ import annotations

from app.models import EstadoReserva, Reserva
from app.store import Almacen


class NoEncontradoError(Exception):
    """El socio o la clase solicitados no existen."""


class ReservaDuplicadaError(Exception):
    """El socio ya tiene una reserva activa para el mismo horario."""

    def __init__(self, mensaje: str = "Ya tenés una reserva activa para ese horario"):
        super().__init__(mensaje)


class ClaseCompletaError(Exception):
    """La clase alcanzó su cupo máximo."""

    def __init__(self, mensaje: str = "Clase completa"):
        super().__init__(mensaje)


class ReservaService:
    def __init__(self, almacen: Almacen) -> None:
        self._almacen = almacen

    def reservar(self, socio_id: str, clase_id: str) -> Reserva:
        socio = self._almacen.obtener_socio(socio_id)
        if socio is None:
            raise NoEncontradoError(f"Socio inexistente: {socio_id}")

        clase = self._almacen.obtener_clase(clase_id)
        if clase is None:
            raise NoEncontradoError(f"Clase inexistente: {clase_id}")

        self._validar_horario_libre(socio_id, clase_id, clase.horario)

        ocupados = self._almacen.reservas_activas_de_clase(clase_id)
        if len(ocupados) >= clase.cupo_maximo:
            raise ClaseCompletaError()

        reserva = Reserva(
            id=self._almacen.siguiente_id_reserva(),
            socio_id=socio_id,
            clase_id=clase_id,
            estado=EstadoReserva.activa,
        )
        return self._almacen.guardar_reserva(reserva)

    def _validar_horario_libre(
        self, socio_id: str, clase_id: str, horario: str
    ) -> None:
        for reserva in self._almacen.reservas_de_socio(socio_id):
            if reserva.estado != EstadoReserva.activa:
                continue
            otra_clase = self._almacen.obtener_clase(reserva.clase_id)
            if otra_clase is None or otra_clase.id == clase_id:
                continue
            if otra_clase.horario == horario:
                raise ReservaDuplicadaError()

    def listar_clases(self) -> list[dict]:
        return [
            {
                "id": clase.id,
                "nombre": clase.nombre,
                "horario": clase.horario,
                "instructor": clase.instructor,
                "cupo_maximo": clase.cupo_maximo,
                "cupos_restantes": self._almacen.cupos_restantes(clase.id),
            }
            for clase in self._almacen.listar_clases()
        ]

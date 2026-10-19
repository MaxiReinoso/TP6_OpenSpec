from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.models import EstadoReserva, Reserva
from app.store import Almacen

VENTANA_CANCELACION = timedelta(hours=2)
DIAS_AUSENCIA = 30
DIAS_BLOQUEO = 7
AUSENCIAS_PARA_BLOQUEO = 3


def _ahora(ahora: datetime | None) -> datetime:
    return ahora if ahora is not None else datetime.now(timezone.utc)


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


class BloqueadoError(Exception):
    """El socio acumuló ausencias suficientes para ser bloqueado."""

    def __init__(self, mensaje: str = "Reservas bloqueadas por acumulación de ausencias"):
        super().__init__(mensaje)


class ReservaService:
    def __init__(self, almacen: Almacen) -> None:
        self._almacen = almacen

    def reservar(self, socio_id: str, clase_id: str, ahora: datetime | None = None) -> Reserva:
        ahora = _ahora(ahora)
        socio = self._almacen.obtener_socio(socio_id)
        if socio is None:
            raise NoEncontradoError(f"Socio inexistente: {socio_id}")

        clase = self._almacen.obtener_clase(clase_id)
        if clase is None:
            raise NoEncontradoError(f"Clase inexistente: {clase_id}")

        self._validar_bloqueo(socio_id, ahora)
        self._validar_horario_libre(socio_id, clase_id, clase.horario)

        ocupados = self._almacen.reservas_ocupantes_de_clase(clase_id)
        if len(ocupados) >= clase.cupo_maximo:
            raise ClaseCompletaError()

        reserva = Reserva(
            id=self._almacen.siguiente_id_reserva(),
            socio_id=socio_id,
            clase_id=clase_id,
            estado=EstadoReserva.activa,
            creada_en=ahora,
        )
        return self._almacen.guardar_reserva(reserva)

    def cancelar(self, reserva_id: str, ahora: datetime | None = None) -> Reserva:
        ahora = _ahora(ahora)
        reserva = self._almacen.obtener_reserva(reserva_id)
        if reserva is None or reserva.estado != EstadoReserva.activa:
            raise NoEncontradoError(f"Reserva inexistente o no activa: {reserva_id}")

        clase = self._almacen.obtener_clase(reserva.clase_id)
        if clase is None:
            raise NoEncontradoError(f"Clase inexistente: {reserva.clase_id}")

        horario = datetime.fromisoformat(clase.horario)
        reserva.estado = (
            EstadoReserva.cancelada
            if horario - ahora >= VENTANA_CANCELACION
            else EstadoReserva.ausente
        )
        return self._almacen.actualizar_reserva(reserva)

    def ausencias(self, socio_id: str, ahora: datetime | None = None) -> list[Reserva]:
        ahora = _ahora(ahora)
        desde = ahora - timedelta(days=DIAS_AUSENCIA)
        return self._ausencias_desde(socio_id, desde)

    def _ausencias_desde(self, socio_id: str, desde: datetime) -> list[Reserva]:
        return [
            r
            for r in self._almacen.reservas_de_socio(socio_id)
            if r.estado == EstadoReserva.ausente and r.creada_en >= desde
        ]

    def _validar_bloqueo(self, socio_id: str, ahora: datetime) -> None:
        ausencias = self._ausencias_desde(
            socio_id, ahora - timedelta(days=DIAS_AUSENCIA)
        )
        if len(ausencias) < AUSENCIAS_PARA_BLOQUEO:
            return
        ultima = max(a.creada_en for a in ausencias)
        if ahora < ultima + timedelta(days=DIAS_BLOQUEO):
            raise BloqueadoError()

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

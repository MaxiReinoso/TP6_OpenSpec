from __future__ import annotations

from app.models import Clase, EstadoReserva, Reserva, Socio


class Almacen:
    """Almacén en memoria de socios, clases y reservas."""

    def __init__(self) -> None:
        self._socios: dict[str, Socio] = {}
        self._clases: dict[str, Clase] = {}
        self._reservas: dict[str, Reserva] = {}
        self._contador = 0

    def agregar_socio(self, socio: Socio) -> Socio:
        self._socios[socio.id] = socio
        return socio

    def agregar_clase(self, clase: Clase) -> Clase:
        self._clases[clase.id] = clase
        return clase

    def obtener_socio(self, socio_id: str) -> Socio | None:
        return self._socios.get(socio_id)

    def obtener_clase(self, clase_id: str) -> Clase | None:
        return self._clases.get(clase_id)

    def listar_clases(self) -> list[Clase]:
        return list(self._clases.values())

    def siguiente_id_reserva(self) -> str:
        self._contador += 1
        return f"res-{self._contador}"

    def guardar_reserva(self, reserva: Reserva) -> Reserva:
        self._reservas[reserva.id] = reserva
        return reserva

    def reservas_de_socio(self, socio_id: str) -> list[Reserva]:
        return [r for r in self._reservas.values() if r.socio_id == socio_id]

    def reservas_activas_de_clase(self, clase_id: str) -> list[Reserva]:
        return [
            r
            for r in self._reservas.values()
            if r.clase_id == clase_id and r.estado == EstadoReserva.activa
        ]

    def cupos_restantes(self, clase_id: str) -> int:
        clase = self.obtener_clase(clase_id)
        if clase is None:
            return 0
        ocupados = len(self.reservas_activas_de_clase(clase_id))
        return max(clase.cupo_maximo - ocupados, 0)

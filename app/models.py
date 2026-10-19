from enum import Enum

from pydantic import BaseModel, Field


class EstadoMembresia(str, Enum):
    activa = "activa"
    inactiva = "inactiva"


class EstadoReserva(str, Enum):
    activa = "activa"
    cancelada = "cancelada"
    ausente = "ausente"


class Socio(BaseModel):
    id: str
    nombre: str
    estado_membresia: EstadoMembresia = EstadoMembresia.activa


class Clase(BaseModel):
    id: str
    nombre: str
    horario: str
    cupo_maximo: int = Field(gt=0)
    instructor: str


class Reserva(BaseModel):
    id: str
    socio_id: str
    clase_id: str
    estado: EstadoReserva = EstadoReserva.activa

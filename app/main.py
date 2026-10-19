from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.models import EstadoMembresia, Socio
from app.service import (
    ClaseCompletaError,
    NoEncontradoError,
    ReservaDuplicadaError,
    ReservaService,
)
from app.store import Almacen


class ReservaRequest(BaseModel):
    socio_id: str
    clase_id: str


def build_app(servicio: ReservaService) -> FastAPI:
    app = FastAPI(title="Reservas de clases grupales")

    @app.exception_handler(NoEncontradoError)
    async def _no_encontrado(_request, exc: NoEncontradoError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ClaseCompletaError)
    async def _clase_completa(_request, exc: ClaseCompletaError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(ReservaDuplicadaError)
    async def _duplicada(_request, exc: ReservaDuplicadaError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.post("/reservas", status_code=201)
    async def crear_reserva(payload: ReservaRequest):
        reserva = servicio.reservar(payload.socio_id, payload.clase_id)
        return reserva.model_dump()

    @app.get("/clases")
    async def listar_clases():
        return servicio.listar_clases()

    return app


def bootstrap() -> FastAPI:
    from app.models import Clase

    almacen = Almacen()
    almacen.agregar_socio(
        Socio(id="socio-1", nombre="Ana", estado_membresia=EstadoMembresia.activa)
    )
    almacen.agregar_clase(
        Clase(
            id="clase-yoga",
            nombre="Yoga",
            horario="18:00",
            cupo_maximo=2,
            instructor="Lucía",
        )
    )
    return build_app(ReservaService(almacen))


app = bootstrap()

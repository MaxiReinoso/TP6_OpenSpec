# Proposal

## Why

Los socios del gimnasio no tienen forma de asegurar su lugar en una clase grupal antes de asistir: al llegar pueden encontrarla completa y perder el viaje. Se necesita que puedan reservar el cupo con anticipación, con una garantía de disponibilidad y reglas claras de exclusividad por horario.

## What Changes

- Nuevo flujo para que un socio reserve su lugar en una clase grupal, descontando el cupo al instante cuando hay disponibilidad.
- Rechazo explícito de la reserva cuando la clase alcanzó su cupo máximo, con el mensaje visible "Clase completa".
- Regla de exclusividad por horario: un socio no puede tener dos reservas activas para el mismo horario, aunque sean clases distintas.
- **Historia de usuario**: Como socio del gimnasio, quiero reservar mi lugar en una clase grupal para asegurarme el cupo antes de ir.

## Capabilities

### New Capabilities
- `reserva-clase`: reserva de cupos en clases grupales por parte de un socio, incluyendo control de disponibilidad, rechazo por clase completa y validación de exclusividad por horario.

### Modified Capabilities
<!-- Sin cambios: el proyecto no cuenta aún con specs existentes. -->

## Impact

- Dominio nuevo de reservas: entidad de reserva (socio, clase, horario, estado activa/cancelada).
- Reglas de negocio: control de cupo disponible y validación de solapamiento por horario por socio.
- Superficie de interacción del socio (reservar clase) y mensajería de error ("Clase completa").
- Sin impacto en código existente: el repositorio está vacío (solo `README.md`) y no hay specs previas.

# Design

## Context

Ver `proposal.md` — Why. El proyecto es greenfield (solo `README.md`) y todavía no existen specs. Este diseño fija el modelo de datos y la decisión de cuándo se consume el cupo, porque determina el resto del comportamiento de reserva.

## Goals / Non-Goals

**Goals:**
- Modelar las entidades del dominio de reservas: `Socio`, `Clase`, `Reserva`.
- Garantizar que el cupo disponible de una `Clase` se valide y descuente al crear la `Reserva`.
- Dejar explícita la regla que impide dos reservas activas del mismo socio en el mismo horario.

**Non-Goals:**
- No define la interfaz de usuario, endpoints ni esquema de code (se resuelve en specs/tasks/implementación).
- No define políticas de cancelación, lista de espera ni cobros.
- No define el mecanismo de notificación o recordatorios.

## Decisions

### Modelo de entidades

- **Socio**: `id`, `nombre`, `estado de membresía`.
- **Clase**: `id`, `nombre`, `horario`, `cupo_máximo`, `instructor`.
- **Reserva**: `socio`, `clase`, `estado` ∈ {`activa`, `cancelada`, `ausente`}.

### Validación y descuento del cupo al crear la Reserva

El cupo de la `Clase` se valida y descuenta en el momento de crear la `Reserva`, no al cierre del día.

**Rationale:** evita que dos socios reserven el mismo último lugar sin saberlo; el segundo intento falla de forma determinista contra el estado real del cupo.

**Alternativas consideradas:**
- *Reservar sin bloquear cupo y validar recién al arrancar la clase.* **Descartada:** permitiría sobreventa visible para el socio, generando reservas que después no se pueden honrar.

## Risks / Trade-offs

- [Descuento inmediato del cupo puede dejar asientos retenidos por reservas nunca usadas] → Mitigación: el estado `ausente` y una política de cancelación (fuera de este change) liberan el cupo.
- [Concurrencia sobre el último cupo disponible] → Mitigación: la validación-descuento debe ejecutarse de forma atómica sobre el cupo de la `Clase`.
- [Regla de exclusividad por horario se restringe a reservas `activa`] → Mitigación: al evaluar colisiones, ignorar reservas `cancelada`.

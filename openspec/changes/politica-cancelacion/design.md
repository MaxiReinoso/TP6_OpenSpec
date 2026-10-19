# Design

## Context

Ver `proposal.md` — Why. Este diseño se apoya en las entidades y el flujo de reserva ya definidos en el change archivado `reservar-clase` (`Socio`, `Clase`, `Reserva`), cuya `Reserva` ya contempla el estado `ausente`.

## Goals / Non-Goals

**Goals:**
- Definir cuándo una cancelación libera el cupo y cuándo no, en función del tiempo restante al horario de la clase.
- Definir cómo se computan las ausencias de un socio y cómo se deriva el bloqueo por reincidencia.

**Non-Goals:**
- No define la interfaz de usuario ni endpoints concretos (se resuelven en specs/tasks/implementación).
- No agrega nuevas entidades ni campos redundantes al modelo.

## Decisions

### Las ausencias se derivan del historial de Reservas

Se usa el estado `ausente` que `Reserva` ya contemplaba. Las ausencias de un `Socio` se calculan a partir de su historial de `Reservas`, **sin agregar un contador redundante**.

**Rationale:** una única fuente de verdad (el historial) evita divergencias entre un contador y los hechos reales de cada reserva.

### La ventana de 2 horas se mide contra el horario de la clase

La ventana de 2 horas se calcula contra el **horario de la clase**, no contra el momento de la cancelación.

**Rationale:** el criterio relevante para liberar el cupo es cuánto falta para que arranque la clase, que es lo que determina si otra persona puede ocupar el lugar.

### Cancelación tardía permitida, pero sin liberar cupo

**Alternativas consideradas:**
- *Bloquear directamente cualquier cancelación tardía.* **Descartada:** un socio con una emergencia real tiene que poder cancelar igual — lo único que cambia según el tiempo restante es si el cupo se libera o no.

## Risks / Trade-offs

- [La ventana depende de una referencia de tiempo confiable] → Mitigación: calcular siempre contra el horario de la clase usando una única fuente de tiempo.
- [El bloqueo por 3 ausencias en 30 días debe reutilizar el historial] → Mitigación: derivar las ausencias de las `Reservas` en el rango de 30 días, sin contadores paralelos.
- [Cancelaciones marcadas `ausente` no liberan cupo y pueden reducir disponibilidad real] → Mitigación: es el comportamiento buscado por la política; el bloqueo desincentiva la reincidencia.

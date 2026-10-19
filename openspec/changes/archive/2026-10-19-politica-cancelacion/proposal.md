# Proposal

## Why

Las ausencias sin aviso dejan cupos que nunca se usan y desalientan a los socios que sí quieren asistir. Se necesita una política de cancelación con plazos y una penalización por reincidencia para liberar cupos reales y desincentivar las ausencias.

## What Changes

- Un socio puede cancelar su reserva hasta **2 horas antes** del horario de la clase, liberando el cupo en ese momento.
- Si cancela con **menos de 2 horas** de anticipación, el cupo **NO** se libera y la reserva queda marcada como `ausencia`.
- Al acumular **3 ausencias en los últimos 30 días**, el sistema **bloquea nuevas reservas** de ese socio por **7 días**.
- **Historia de usuario**: Como administrador del gimnasio, quiero penalizar las ausencias sin aviso para liberar cupos reales a quienes sí van a asistir.

## Capabilities

### New Capabilities
- `politica-cancelacion`: cancelación de reservas con ventana de 2 horas (libera o no el cupo) y bloqueo temporal del socio tras 3 ausencias en 30 días.

### Modified Capabilities
- `reservar-clase`: la reserva ahora debe rechazarse cuando el socio está bloqueado por acumulación de ausencias.

## Impact

- Estado de `Reserva` ya previsto en el modelo (`activa` / `cancelada` / `ausente`) pasa a usarse: cancelación tardía marca `ausente`.
- Cálculo de cupo: una cancelación a tiempo libera cupo; las ausencias no.
- Nuevo registro de eventos de cancelación con marca de tiempo para computar la ventana de 30 días y el bloqueo de 7 días.
- Superficie de administración/socio: cancelar reserva y consultar estado de bloqueo.
- Depende de las entidades y del flujo de reserva existentes del change archivado `reservar-clase`.

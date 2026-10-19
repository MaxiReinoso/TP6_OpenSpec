# Spec Delta

## Purpose

Define la política de cancelación de reservas y la penalización por ausencias: cuándo libera cupo, cuándo se registra ausencia y cuándo se bloquea el socio por reincidencia.

## ADDED Requirements

### Requirement: Cancelación y penalización por ausencia

El sistema SHALL permitir al socio cancelar su reserva, liberando el cupo cuando se hace con la anticipación requerida y registrando la ausencia cuando no.

#### Scenario: Cancelación tardía

- **WHEN** el socio cancela su reserva con menos de 2 horas de anticipación al horario de la clase
- **THEN** el sistema marca la reserva como "ausencia" y no libera el cupo

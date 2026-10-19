# reservar-clase Specification

## Purpose

Permite que un socio reserve su lugar en una clase grupal asegurando el cupo antes de asistir, con control de disponibilidad al momento de reservar.

## Requirements

### Requirement: Reserva de turno a clase grupal

El sistema SHALL permitir al socio reservar un turno en una clase grupal, validando y descontando el cupo disponible al momento de crear la reserva.

#### Scenario: Clase completa

- **WHEN** el socio intenta reservar una clase que ya alcanzó su cupo máximo
- **THEN** el sistema rechaza la reserva y muestra "Clase completa", sin descontar cupo

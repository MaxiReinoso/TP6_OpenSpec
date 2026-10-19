# Tasks

## 1. Modelo de datos

- [ ] 1.1 Modelo de datos de Clase y Reserva (según `design.md`: Clase con id, nombre, horario, cupo_máximo, instructor; Reserva con socio, clase, estado activa/cancelada/ausente) y verificar que las entidades se persisten y recuperan correctamente

## 2. Reserva

- [ ] 2.1 Endpoint de reserva con validación de cupo disponible y verificar que, con cupo disponible, la reserva se crea y el cupo se descuenta en el momento
- [ ] 2.2 Validación de reserva duplicada en el mismo horario y verificar que el sistema rechaza una segunda reserva activa del mismo socio en el mismo horario aunque sea otra clase

## 3. Disponibilidad

- [ ] 3.1 Endpoint de listado de clases con cupos restantes y verificar que el listado refleja el cupo restante tras cada reserva

## 4. Tests

- [ ] 4.1 Tests de los tres criterios de aceptación y verificar que los tres casos (reserva con cupo disponible descuenta cupo, clase completa rechaza con "Clase completa" sin descontar cupo, reserva duplicada en el mismo horario se rechaza) pasan en verde

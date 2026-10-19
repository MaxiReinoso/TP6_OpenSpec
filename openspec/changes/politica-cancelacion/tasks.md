# Tasks

## 1. Cancelación

- [ ] 1.1 Endpoint de cancelación con validación de ventana de 2 horas y verificar que, con más de 2 horas de anticipación, la cancelación libera el cupo y, con menos de 2 horas, la reserva queda marcada como "ausencia" sin liberar cupo

## 2. Ausencias

- [ ] 2.1 Cálculo de ausencias de un socio en los últimos 30 días a partir del historial de Reservas y verificar que el conteo refleja únicamente las reservas en estado "ausente" dentro de la ventana

## 3. Bloqueo

- [ ] 3.1 Bloqueo de nuevas reservas por 7 días al llegar a 3 ausencias y verificar que el sistema rechaza nuevas reservas del socio durante el bloqueo

## 4. Tests

- [ ] 4.1 Tests de los tres criterios de aceptación y verificar que los tres casos (cancelar a tiempo libera el cupo, cancelar tardío marca ausencia sin liberar cupo, 3 ausencias en 30 días bloquean 7 días) pasan en verde

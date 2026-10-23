# Demo: Replay Attack sobre token de confirmación reutilizable

**Curso:** Parcial 1 — Amenazas y riesgos; metodología y automatización; corrección y regresión
**Participantes:** Alexander y Josue
**Duración del video:** 7 minutos (3 min teoría + 4 min práctica)
**Commit mostrado:** `demo/replay-fix`

---

## Objetivo

Demostrar un **replay attack** sobre un token de confirmación reutilizable en una API de reservas, aplicar un control de **token de un solo uso con expiración**, y verificar la diferencia entre el antes y el después.

## Problema

El endpoint `/reservar/confirmar-vulnerable` acepta el mismo token múltiples veces porque:

- no verifica si el token ya fue consumido;
- no verifica si el token expiró.

Esto permite que una solicitud válida capturada sea reenviada y aceptada nuevamente, alterando el estado de la reserva sin autorización.

## Solución aplicada

El endpoint corregido `/reservar/confirmar` agrega tres verificaciones en orden:

1. Token válido.
2. Token no utilizado previamente (`token_usado == False`).
3. Token no expirado (`datetime.now() <= token_expira`).

Solo si pasa las tres, marca la reserva como confirmada y pone `token_usado = True`.

---

## Estructura del proyecto

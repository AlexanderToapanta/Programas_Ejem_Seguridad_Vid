from fastapi import FastAPI, Depends, HTTPException

from app.auth import autenticar
from app.database import find_reserva_por_id, find_reserva_de_usuario
from app.logger import registrar_acceso_denegado

app = FastAPI(title="Hotel Los Alerces - Reservas")


# ---------------------------------------------------------
# VERSIÓN VULNERABLE (antes del control)
# ---------------------------------------------------------
@app.get("/api/reservas/vulnerable/{reserva_id}")
async def obtener_reserva_vulnerable(reserva_id: int, usuario=Depends(autenticar)):
    # Autentica, pero NO verifica propiedad -> IDOR
    reserva = find_reserva_por_id(reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva


# ---------------------------------------------------------
# VERSIÓN CORREGIDA (después del control)
# ---------------------------------------------------------
@app.get("/api/reservas/{reserva_id}")
async def obtener_reserva(reserva_id: int, usuario=Depends(autenticar)):
    # CONTROL PREVENTIVO: filtro por usuario_id en la consulta
    reserva = find_reserva_de_usuario(reserva_id, usuario["id"])

    if not reserva:
        # CONTROL DETECTIVO: registrar el intento denegado
        # (si la reserva existe pero es de otro, o si no existe)
        if find_reserva_por_id(reserva_id) is not None:
            registrar_acceso_denegado(usuario["id"], reserva_id)

        # 404 en ambos casos: no revelar si la reserva existe
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    return reserva
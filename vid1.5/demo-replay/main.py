from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI(title="Demo Replay Attack - Reservas Restaurante")

reservas_db = {
    "R001": {
        "estado": "pendiente",
        "token": "confirma-demo-123",
        "token_usado": False,
        "token_expira": datetime.now() + timedelta(minutes=5),
    }
}

class Confirmacion(BaseModel):
    reserva_id: str
    token: str

# ---------- ENDPOINT VULNERABLE (prueba ANTES) ----------
@app.post("/reservar/confirmar-vulnerable")
def confirmar_vulnerable(datos: Confirmacion):
    reserva = reservas_db.get(datos.reserva_id)
    if not reserva or reserva["token"] != datos.token:
        raise HTTPException(status_code=403, detail="Token inválido")
    # No verifica si el token ya fue usado ni si expiró  <-- Pregunta 2 (Josue)
    reserva["estado"] = "confirmada"
    return {"mensaje": "Reserva confirmada", "estado": reserva["estado"]}

# ---------- ENDPOINT CORREGIDO (prueba DESPUÉS) ----------
@app.post("/reservar/confirmar")
def confirmar_seguro(datos: Confirmacion):
    reserva = reservas_db.get(datos.reserva_id)
    if not reserva or reserva["token"] != datos.token:
        raise HTTPException(status_code=403, detail="Token inválido")
    if reserva["token_usado"]:  # <-- Pregunta 3 (Josue)
        raise HTTPException(status_code=409, detail="Token ya utilizado")
    if datetime.now() > reserva["token_expira"]:
        raise HTTPException(status_code=410, detail="Token expirado")
    reserva["estado"] = "confirmada"
    reserva["token_usado"] = True
    return {"mensaje": "Reserva confirmada", "estado": reserva["estado"]}

@app.post("/reservar/reset")
def reset_reserva():
    reservas_db["R001"] = {
        "estado": "pendiente",
        "token": "confirma-demo-123",
        "token_usado": False,
        "token_expira": datetime.now() + timedelta(minutes=5),
    }
    return {"mensaje": "Reserva reiniciada para nueva prueba"}
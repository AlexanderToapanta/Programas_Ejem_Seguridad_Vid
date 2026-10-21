"""
VERSIÓN CON CONTROL.

Controles aplicados:
1. Autorización por recurso: solo el dueño o un docente accede a las notas.
2. Validación de rol: solo docentes modifican nota_final.
"""
from fastapi import Depends, FastAPI, HTTPException

from app.auth import autenticar
from app.database import NOTAS_DB
from app.schemas import ActualizarNota

app = FastAPI(title="API Notas - Segura")


@app.get("/api/notas/{estudiante_id}")
def obtener_notas(estudiante_id: int, usuario: dict = Depends(autenticar)):
    # CONTROL 1: autorización por recurso
    if usuario["id"] != estudiante_id and usuario["rol"] != "docente":
        raise HTTPException(403, "No autorizado")
    if estudiante_id not in NOTAS_DB:
        raise HTTPException(404, "Estudiante no encontrado")
    return NOTAS_DB[estudiante_id]


@app.put("/api/notas/{estudiante_id}")
def actualizar_nota(
    estudiante_id: int,
    datos: ActualizarNota,
    usuario: dict = Depends(autenticar),
):
    # CONTROL 2: solo docentes modifican notas
    if usuario["rol"] != "docente":
        raise HTTPException(403, "Solo docentes pueden modificar notas")
    if estudiante_id not in NOTAS_DB:
        raise HTTPException(404, "Estudiante no encontrado")
    NOTAS_DB[estudiante_id]["nota_final"] = datos.nota_final
    return {"ok": True, "nueva_nota": NOTAS_DB[estudiante_id]["nota_final"]}
"""
VERSIÓN VULNERABLE — solo demostración educativa.

Vulnerabilidades intencionales:
1. Confidencialidad: no verifica que el token pertenezca al estudiante_id.
2. Integridad: cualquier usuario autenticado puede modificar nota_final.
"""
from fastapi import FastAPI, HTTPException

from app.database import NOTAS_DB
from app.schemas import ActualizarNota

app = FastAPI(title="API Notas - Vulnerable")


@app.get("/api/notas/{estudiante_id}")
def obtener_notas(estudiante_id: int, token: str):
    # No valida que `token` corresponda a `estudiante_id`
    if estudiante_id not in NOTAS_DB:
        raise HTTPException(404, "Estudiante no encontrado")
    return NOTAS_DB[estudiante_id]


@app.put("/api/notas/{estudiante_id}")
def actualizar_nota(estudiante_id: int, token: str, datos: ActualizarNota):
    # No valida rol: cualquier token modifica la nota
    if estudiante_id not in NOTAS_DB:
        raise HTTPException(404, "Estudiante no encontrado")
    NOTAS_DB[estudiante_id]["nota_final"] = datos.nota_final
    return {"ok": True, "nueva_nota": NOTAS_DB[estudiante_id]["nota_final"]}
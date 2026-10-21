"""
VERSIÓN VULNERABLE — solo para demostración educativa.
No usar en producción.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="API Notas - Vulnerable")

# Base de datos ficticia en memoria
NOTAS_DB = {
    1001: {"estudiante_id": 1001, "nombre": "Ana Torres", "nota_final": 70},
    1002: {"estudiante_id": 1002, "nombre": "Luis Pérez", "nota_final": 85},
}

# Simulación de usuarios autenticados (en la vida real vendría del JWT)
USUARIOS = {
    "token-ana":   {"id": 1001, "rol": "estudiante"},
    "token-luis":  {"id": 1002, "rol": "estudiante"},
    "token-docente": {"id": 9000, "rol": "docente"},
}


class ActualizarNota(BaseModel):
    nota_final: int


@app.get("/api/notas/{estudiante_id}")
def obtener_notas(estudiante_id: int, token: str):
    # VULNERABILIDAD 1: no verifica que el token pertenezca al estudiante_id
    if estudiante_id not in NOTAS_DB:
        raise HTTPException(404, "Estudiante no encontrado")
    return NOTAS_DB[estudiante_id]


@app.put("/api/notas/{estudiante_id}")
def actualizar_nota(estudiante_id: int, token: str, datos: ActualizarNota):
    # VULNERABILIDAD 2: cualquier usuario autenticado puede modificar nota_final
    if estudiante_id not in NOTAS_DB:
        raise HTTPException(404, "Estudiante no encontrado")
    NOTAS_DB[estudiante_id]["nota_final"] = datos.nota_final
    return {"ok": True, "nueva_nota": NOTAS_DB[estudiante_id]["nota_final"]}
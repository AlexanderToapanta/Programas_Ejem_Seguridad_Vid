"""
VERSIÓN CON CONTROL — aplica autorización por recurso y validación de rol.
"""
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel

app = FastAPI(title="API Notas - Segura")

NOTAS_DB = {
    1001: {"estudiante_id": 1001, "nombre": "Ana Torres", "nota_final": 70},
    1002: {"estudiante_id": 1002, "nombre": "Luis Pérez", "nota_final": 85},
}

USUARIOS = {
    "token-ana":     {"id": 1001, "rol": "estudiante"},
    "token-luis":    {"id": 1002, "rol": "estudiante"},
    "token-docente": {"id": 9000, "rol": "docente"},
}


def autenticar(authorization: str = Header(...)) -> dict:
    """Extrae el token del header Authorization: Bearer <token>."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Formato de token inválido")
    token = authorization.removeprefix("Bearer ").strip()
    usuario = USUARIOS.get(token)
    if not usuario:
        raise HTTPException(401, "Token inválido")
    return usuario


class ActualizarNota(BaseModel):
    # Solo se acepta este campo; el rol se valida aparte
    nota_final: int


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
    # CONTROL 2: solo docentes pueden modificar notas
    if usuario["rol"] != "docente":
        raise HTTPException(403, "Solo docentes pueden modificar notas")
    if estudiante_id not in NOTAS_DB:
        raise HTTPException(404, "Estudiante no encontrado")
    NOTAS_DB[estudiante_id]["nota_final"] = datos.nota_final
    return {"ok": True, "nueva_nota": NOTAS_DB[estudiante_id]["nota_final"]}
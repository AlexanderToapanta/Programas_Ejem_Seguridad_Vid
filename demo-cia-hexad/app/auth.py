"""
Autenticación simulada por token en header Authorization.
En producción esto sería verificación de JWT firmado.
"""
from fastapi import Header, HTTPException

from app.database import USUARIOS


def autenticar(authorization: str = Header(...)) -> dict:
    """
    Extrae el token del header `Authorization: Bearer <token>`.
    Devuelve el usuario asociado o lanza 401.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Formato de token inválido")
    token = authorization.removeprefix("Bearer ").strip()
    usuario = USUARIOS.get(token)
    if usuario is None:
        raise HTTPException(401, "Token inválido")
    return usuario
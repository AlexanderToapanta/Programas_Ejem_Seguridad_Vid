from fastapi import Header, HTTPException
from app.database import USUARIOS


async def autenticar(authorization: str = Header(default="")):
    """
    Espera el header:  Authorization: Bearer <token>
    Devuelve el usuario autenticado o 401.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token requerido")

    token = authorization.replace("Bearer ", "").strip()

    for usuario in USUARIOS.values():
        if usuario["token"] == token:
            return usuario

    raise HTTPException(status_code=401, detail="Token inválido")
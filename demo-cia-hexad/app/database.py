"""
Base de datos ficticia en memoria.
Se reinicia al importar el módulo.
"""

NOTAS_DB: dict[int, dict] = {
    1001: {"estudiante_id": 1001, "nombre": "Ana Torres", "nota_final": 70},
    1002: {"estudiante_id": 1002, "nombre": "Luis Pérez", "nota_final": 85},
}

USUARIOS: dict[str, dict] = {
    "token-ana":     {"id": 1001, "rol": "estudiante"},
    "token-luis":    {"id": 1002, "rol": "estudiante"},
    "token-docente": {"id": 9000, "rol": "docente"},
}


def reset_db() -> None:
    """Restaura los valores originales. Usado por las pruebas."""
    NOTAS_DB[1001]["nota_final"] = 70
    NOTAS_DB[1002]["nota_final"] = 85
# Reservas ficticias: id secuencial (esto es parte del problema IDOR)
RESERVAS = [
    {"id": 1001, "usuario_id": "ana",    "titular": "Ana Pérez",    "habitacion": "204"},
    {"id": 1002, "usuario_id": "carlos", "titular": "Carlos Ruiz",  "habitacion": "310"},
    {"id": 1003, "usuario_id": "maria",  "titular": "María López",  "habitacion": "115"},
]

# Usuarios ficticios y su token (en un caso real NUNCA se guarda así)
USUARIOS = {
    "ana":    {"id": "ana",    "token": "token-ficticio-ana"},
    "carlos": {"id": "carlos", "token": "token-ficticio-carlos"},
    "maria":  {"id": "maria",  "token": "token-ficticio-maria"},
}


def find_reserva_por_id(reserva_id: int):
    """Devuelve una reserva por ID (versión vulnerable: sin filtrar por usuario)."""
    for r in RESERVAS:
        if r["id"] == reserva_id:
            return r
    return None


def find_reserva_de_usuario(reserva_id: int, usuario_id: str):
    """Devuelve una reserva SOLO si pertenece al usuario (control preventivo)."""
    for r in RESERVAS:
        if r["id"] == reserva_id and r["usuario_id"] == usuario_id:
            return r
    return None
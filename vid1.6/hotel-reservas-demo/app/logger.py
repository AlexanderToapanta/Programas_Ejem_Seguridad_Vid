import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/accesos.log",
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("hotel")


def registrar_acceso_denegado(usuario_id: str, reserva_id: int):
    logger.warning(
        f"Acceso denegado | usuario={usuario_id} | reserva_solicitada={reserva_id}"
    )
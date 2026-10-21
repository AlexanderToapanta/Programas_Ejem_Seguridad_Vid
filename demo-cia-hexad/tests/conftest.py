"""Fixtures compartidos por las pruebas."""
import pytest

from app.database import reset_db


@pytest.fixture(autouse=True)
def limpiar_bd():
    """Restaura la BD antes de cada prueba."""
    reset_db()
    yield
    reset_db()
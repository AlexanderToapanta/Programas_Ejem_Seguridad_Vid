"""Demuestra que la versión vulnerable rompe CIA."""
from fastapi.testclient import TestClient

from app.vulnerable import app

client = TestClient(app)


def test_confidencialidad_rota():
    """Ana (1001) lee las notas de Luis (1002)."""
    r = client.get("/api/notas/1002", params={"token": "token-ana"})
    assert r.status_code == 200
    assert r.json()["estudiante_id"] == 1002  # fuga


def test_integridad_rota():
    """Ana modifica su propia nota a 100."""
    r = client.put(
        "/api/notas/1001",
        params={"token": "token-ana"},
        json={"nota_final": 100},
    )
    assert r.status_code == 200
    assert r.json()["nueva_nota"] == 100
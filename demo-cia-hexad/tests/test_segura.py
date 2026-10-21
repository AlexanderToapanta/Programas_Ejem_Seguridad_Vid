"""Demuestra que la versión segura preserva CIA."""
import time

from fastapi.testclient import TestClient

from app.segura import app

client = TestClient(app)


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_confidencialidad_preservada():
    """Ana NO lee las notas de Luis."""
    r = client.get("/api/notas/1002", headers=auth("token-ana"))
    assert r.status_code == 403


def test_acceso_propio_permitido():
    """Ana lee sus propias notas."""
    r = client.get("/api/notas/1001", headers=auth("token-ana"))
    assert r.status_code == 200
    assert r.json()["estudiante_id"] == 1001


def test_docente_accede_a_cualquiera():
    """El docente lee las notas de cualquier estudiante."""
    r = client.get("/api/notas/1002", headers=auth("token-docente"))
    assert r.status_code == 200


def test_integridad_preservada():
    """Ana NO modifica su nota."""
    r = client.put(
        "/api/notas/1001",
        headers=auth("token-ana"),
        json={"nota_final": 100},
    )
    assert r.status_code == 403


def test_docente_modifica_nota():
    """El docente sí modifica notas."""
    r = client.put(
        "/api/notas/1001",
        headers=auth("token-docente"),
        json={"nota_final": 95},
    )
    assert r.status_code == 200
    assert r.json()["nueva_nota"] == 95


def test_disponibilidad_basica():
    """La API responde en menos de 200 ms."""
    inicio = time.perf_counter()
    r = client.get("/api/notas/1001", headers=auth("token-ana"))
    duracion_ms = (time.perf_counter() - inicio) * 1000
    assert r.status_code == 200
    assert duracion_ms < 200
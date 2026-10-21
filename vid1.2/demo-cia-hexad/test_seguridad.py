"""
Pruebas que demuestran el antes y el después.
Ejecutar: pytest -v test_seguridad.py
"""
import pytest
from fastapi.testclient import TestClient

import app_vulnerable
import app_segura


@pytest.fixture(autouse=True)
def reset_db():
    """Restaura la BD antes de cada prueba."""
    for mod in (app_vulnerable, app_segura):
        mod.NOTAS_DB[1001]["nota_final"] = 70
        mod.NOTAS_DB[1002]["nota_final"] = 85


# ---------- PRUEBAS SOBRE LA VERSIÓN VULNERABLE ----------

def test_vulnerable_confidencialidad_rota():
    """Ana (1001) puede leer las notas de Luis (1002)."""
    client = TestClient(app_vulnerable.app)
    r = client.get("/api/notas/1002", params={"token": "token-ana"})
    assert r.status_code == 200
    assert r.json()["estudiante_id"] == 1002  # ¡fuga de datos!


def test_vulnerable_integridad_rota():
    """Ana puede modificar su propia nota a 100."""
    client = TestClient(app_vulnerable.app)
    r = client.put(
        "/api/notas/1001",
        params={"token": "token-ana"},
        json={"nota_final": 100},
    )
    assert r.status_code == 200
    assert r.json()["nueva_nota"] == 100  # ¡integridad rota!


# ---------- PRUEBAS SOBRE LA VERSIÓN SEGURA ----------

def test_segura_confidencialidad_preservada():
    """Ana NO puede leer las notas de Luis."""
    client = TestClient(app_segura.app)
    r = client.get(
        "/api/notas/1002",
        headers={"Authorization": "Bearer token-ana"},
    )
    assert r.status_code == 403


def test_segura_acceso_propio_permitido():
    """Ana sí puede leer sus propias notas."""
    client = TestClient(app_segura.app)
    r = client.get(
        "/api/notas/1001",
        headers={"Authorization": "Bearer token-ana"},
    )
    assert r.status_code == 200
    assert r.json()["estudiante_id"] == 1001


def test_segura_docente_accede_a_cualquiera():
    """El docente puede leer las notas de cualquier estudiante."""
    client = TestClient(app_segura.app)
    r = client.get(
        "/api/notas/1002",
        headers={"Authorization": "Bearer token-docente"},
    )
    assert r.status_code == 200


def test_segura_integridad_preservada():
    """Ana NO puede modificar su nota."""
    client = TestClient(app_segura.app)
    r = client.put(
        "/api/notas/1001",
        headers={"Authorization": "Bearer token-ana"},
        json={"nota_final": 100},
    )
    assert r.status_code == 403
    # Verifica que la nota no cambió
    assert app_segura.NOTAS_DB[1001]["nota_final"] == 70


def test_segura_docente_modifica_nota():
    """El docente sí puede modificar notas."""
    client = TestClient(app_segura.app)
    r = client.put(
        "/api/notas/1001",
        headers={"Authorization": "Bearer token-docente"},
        json={"nota_final": 95},
    )
    assert r.status_code == 200
    assert r.json()["nueva_nota"] == 95


def test_disponibilidad_respuesta_rapida():
    """La API responde en menos de 200 ms (disponibilidad básica)."""
    import time
    client = TestClient(app_segura.app)
    inicio = time.perf_counter()
    r = client.get(
        "/api/notas/1001",
        headers={"Authorization": "Bearer token-ana"},
    )
    duracion_ms = (time.perf_counter() - inicio) * 1000
    assert r.status_code == 200
    assert duracion_ms < 200
import subprocess
import time
import requests
import pytest

BASE = "http://127.0.0.1:5001"
USUARIO_A = "usuario_A"
USUARIO_B = "usuario_B"


@pytest.fixture(scope="module", autouse=True)
def servidor():
    proc = subprocess.Popen(
        ["python", "app_corregida.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2.5)
    yield
    proc.terminate()
    proc.wait()


def bloquear(usuario, asiento):
    return requests.post(
        f"{BASE}/api/bloquear-asiento",
        json={"id_usuario": usuario, "id_asiento": asiento}
    )


def test_usuario_a_puede_bloquear_dos():
    assert bloquear(USUARIO_A, 1).status_code == 200
    assert bloquear(USUARIO_A, 2).status_code == 200


def test_usuario_a_tercer_bloqueo_rechazado():
    r = bloquear(USUARIO_A, 3)
    assert r.status_code == 429
    assert r.json()["error"] == "límite de bloqueos excedido"


def test_usuario_b_no_afectado():
    assert bloquear(USUARIO_B, 4).status_code == 200
    assert bloquear(USUARIO_B, 5).status_code == 200
    assert bloquear(USUARIO_B, 6).status_code == 429
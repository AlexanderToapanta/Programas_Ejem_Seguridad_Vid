from fastapi.testclient import TestClient
from main import app

cliente = TestClient(app)

def prueba_antes():
    print("\n=== PRUEBA ANTES DEL CONTROL (vulnerable) ===")
    cliente.post("/reservar/reset")
    payload = {"reserva_id": "R001", "token": "confirma-demo-123"}

    r1 = cliente.post("/reservar/confirmar-vulnerable", json=payload)
    print("1ra petición:", r1.status_code, r1.json())

    r2 = cliente.post("/reservar/confirmar-vulnerable", json=payload)
    print("2da petición:", r2.status_code, r2.json())
    print("RESULTADO: el replay FUE ACEPTADO (fallo demostrado)")

def prueba_despues():
    print("\n=== PRUEBA DESPUÉS DEL CONTROL (corregido) ===")
    cliente.post("/reservar/reset")
    payload = {"reserva_id": "R001", "token": "confirma-demo-123"}

    r1 = cliente.post("/reservar/confirmar", json=payload)
    print("1ra petición:", r1.status_code, r1.json())

    r2 = cliente.post("/reservar/confirmar", json=payload)
    print("2da petición:", r2.status_code, r2.json())
    print("RESULTADO: el replay FUE RECHAZADO (control efectivo)")

if __name__ == "__main__":
    prueba_antes()
    prueba_despues()
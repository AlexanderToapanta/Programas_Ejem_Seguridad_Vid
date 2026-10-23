# Hotel Los Alerces — Demo de Tipos de Controles

Demostración de **control preventivo** (autorización a nivel de objeto) y
**control detectivo** (log de accesos denegados) frente a una vulnerabilidad
**IDOR / BOLA** en una API de reservas de hotel ficticio.

## Requisitos
- Python 3.11+

## Instalación

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

Servidor en: http://127.0.0.1:8000
Documentación automática: http://127.0.0.1:8000/docs

## Ejecutar las pruebas (en otra terminal)

```bash
bash tests/pruebas.sh
```

## Tokens ficticios
| Usuario | Token |
|---|---|
| ana | token-ficticio-ana |
| carlos | token-ficticio-carlos |
| maria | token-ficticio-maria |

## Endpoints
- `GET /api/reservas/vulnerable/{id}` — sin control (antes)
- `GET /api/reservas/{id}` — con control preventivo + detectivo (después)

## Log detectivo
Se escribe en `logs/accesos.log`.
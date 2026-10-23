# Ticketing Demo — Amenaza, vulnerabilidad, riesgo y ataque

Ejemplo práctico del video: API de bloqueo de asientos para una plataforma
de venta de entradas en línea.

## Archivos

- `app_vulnerable.py` — versión sin límite de bloqueos por usuario (puerto 5000)
- `app_corregida.py` — versión con límite de 2 bloqueos por usuario (puerto 5001)
- `test_verificacion.py` — prueba automática del control

## Ejecución

```bash
pip install -r requirements.txt
python app_vulnerable.py     # demostración del ataque
python app_corregida.py      # versión con control
pytest test_verificacion.py -v
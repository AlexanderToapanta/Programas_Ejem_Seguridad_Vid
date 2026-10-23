"""Demuestra que si alguien altera una fila, la cadena se rompe.
Uso:
    python verificar_integridad.py          -> verifica
    python verificar_integridad.py tamper   -> altera una fila y verifica
"""
import sys
from app.db import get_conn
from app.audit import verify_chain

if len(sys.argv) > 1 and sys.argv[1] == "tamper":
    conn = get_conn()
    # Alteramos el resultado de la primera entrada (simula manipulación)
    conn.execute("""
        UPDATE audit_log
        SET result = 'SUCCESS'
        WHERE id = (SELECT MIN(id) FROM audit_log)
    """)
    conn.commit()
    conn.close()
    print(">> Se alteró la fila más antigua de audit_log (result -> SUCCESS)\n")

ok, detalle = verify_chain()
print(detalle)
print("RESULTADO:", "OK" if ok else "CADENA ROTA (manipulación detectada)")
sys.exit(0 if ok else 1)
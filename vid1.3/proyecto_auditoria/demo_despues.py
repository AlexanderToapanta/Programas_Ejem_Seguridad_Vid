from app.db import reset_db, seed, get_conn
from app.courses import drop_course
from app.audit import verify_chain

reset_db()
seed()

print("=== PRUEBA DESPUÉS DEL CONTROL ===")

# Sesión simulada del estudiante
SESSION = "sess_7f3a"
IP = "10.0.2.15"
UA = "Mozilla/5.0 (Demo)"

# 1) Baja válida
r1 = drop_course("est123", "CS101", IP, UA, SESSION)
print("Resultado 1:", r1)

# 2) Segundo intento sobre el mismo curso (ya no inscrito)
r2 = drop_course("est123", "CS101", IP, UA, SESSION)
print("Resultado 2:", r2)

print("\n--- audit_log ---")
rows = get_conn().execute("""
    SELECT ts, event, student_id, course_id, ip, session_id,
           correlation_id, result, reason, prev_hash, entry_hash
    FROM audit_log ORDER BY id
""").fetchall()

for r in rows:
    ts, event, student, course, ip, sess, corr, result, reason, prev_h, entry_h = r
    print(f"{ts} | {event:<20} | student={student} | course={course} | "
          f"ip={ip} | session={sess} | result={result:<12} | corr={corr[:8]}...")
    print(f"    prev_hash={prev_h[:16]}...  entry_hash={entry_h[:16]}...")

print("\n--- verificación de integridad ---")
ok, detalle = verify_chain()
print(detalle)
assert ok, "La cadena de integridad NO es válida"
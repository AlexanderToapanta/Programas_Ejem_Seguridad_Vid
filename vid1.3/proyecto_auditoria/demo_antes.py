from app.db import reset_db, seed, get_conn
from app.courses import drop_course_antes

reset_db()
seed()

print("=== PRUEBA ANTES DEL CONTROL ===")
print("Inscripciones iniciales:", get_conn().execute(
    "SELECT * FROM enrollments").fetchall())

drop_course_antes("est123", "CS101")

print("Inscripciones después:", get_conn().execute(
    "SELECT * FROM enrollments").fetchall())

print("\nLog de auditoría (debería estar vacío):")
print(get_conn().execute("SELECT * FROM audit_log").fetchall())
print("\n>>> No hay forma de demostrar quién hizo la baja, cuándo, ni desde dónde.")
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "auditoria.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # Tabla de inscripciones (negocio)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            student_id TEXT NOT NULL,
            course_id  TEXT NOT NULL,
            PRIMARY KEY (student_id, course_id)
        )
    """)

    # Tabla de auditoría: append-only a nivel de aplicación
    # (permisos reales se configuran a nivel de BD/OS; ver sección 6)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            ts             TEXT NOT NULL,
            event          TEXT NOT NULL,
            student_id     TEXT,
            course_id      TEXT,
            ip             TEXT,
            user_agent     TEXT,
            session_id     TEXT,
            correlation_id TEXT,
            result         TEXT,
            reason         TEXT,
            prev_hash      TEXT,
            entry_hash     TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def reset_db():
    """Borra la BD para reiniciar la demo (uso solo en clase)."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()


def seed():
    """Datos ficticios: un estudiante inscrito en un curso."""
    conn = get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO enrollments (student_id, course_id) VALUES (?, ?)",
        ("est123", "CS101"),
    )
    conn.commit()
    conn.close()
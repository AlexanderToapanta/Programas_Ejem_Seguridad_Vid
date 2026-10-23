import hashlib
import json

from .db import get_conn


def _last_hash(conn):
    cur = conn.execute("SELECT entry_hash FROM audit_log ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    return row[0] if row else "GENESIS"


def _build_entry(ts, event, student_id, course_id, ip, user_agent,
                 session_id, correlation_id, result, reason):
    # Representación canónica y determinista del contenido
    payload = {
        "ts": ts,
        "event": event,
        "student_id": student_id,
        "course_id": course_id,
        "ip": ip,
        "user_agent": user_agent,
        "session_id": session_id,
        "correlation_id": correlation_id,
        "result": result,
        "reason": reason,
    }
    return json.dumps(payload, sort_keys=True, ensure_ascii=False)


def log_event(event, student_id, course_id, ip, user_agent,
              session_id, correlation_id, ts, result, reason=""):
    """Inserta una entrada de auditoría encadenada por hash.

    - Integridad: entry_hash = SHA256(prev_hash || contenido_canónico)
    - Append-only a nivel de aplicación: no hay UPDATE/DELETE aquí.
    """
    conn = get_conn()
    try:
        prev_hash = _last_hash(conn)
        content = _build_entry(ts, event, student_id, course_id, ip, user_agent,
                               session_id, correlation_id, result, reason)
        entry_hash = hashlib.sha256((prev_hash + content).encode("utf-8")).hexdigest()

        conn.execute("""
            INSERT INTO audit_log
            (ts, event, student_id, course_id, ip, user_agent,
             session_id, correlation_id, result, reason, prev_hash, entry_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ts, event, student_id, course_id, ip, user_agent,
              session_id, correlation_id, result, reason, prev_hash, entry_hash))
        conn.commit()
    finally:
        conn.close()


def verify_chain():
    """Recalcula la cadena y compara con lo almacenado.

    Devuelve (ok: bool, detalle: str)
    """
    conn = get_conn()
    try:
        rows = conn.execute("""
            SELECT id, ts, event, student_id, course_id, ip, user_agent,
                   session_id, correlation_id, result, reason, prev_hash, entry_hash
            FROM audit_log ORDER BY id ASC
        """).fetchall()
    finally:
        conn.close()

    expected_prev = "GENESIS"
    for r in rows:
        (row_id, ts, event, student_id, course_id, ip, user_agent,
         session_id, correlation_id, result, reason, prev_hash, entry_hash) = r

        if prev_hash != expected_prev:
            return False, f"Fila {row_id}: prev_hash no coincide con el hash anterior."

        content = _build_entry(ts, event, student_id, course_id, ip, user_agent,
                               session_id, correlation_id, result, reason)
        recalculated = hashlib.sha256((prev_hash + content).encode("utf-8")).hexdigest()
        if recalculated != entry_hash:
            return False, f"Fila {row_id}: entry_hash recalculado no coincide (contenido alterado)."

        expected_prev = entry_hash

    return True, f"INTEGRITY OK ({len(rows)} entradas verificadas)"
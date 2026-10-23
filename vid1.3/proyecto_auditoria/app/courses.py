import datetime
import uuid

from .db import get_conn
from .audit import log_event


# ---------------------------------------------------------------
# VERSIÓN ANTES (para la "prueba previa")
# ---------------------------------------------------------------
def drop_course_antes(student_id, course_id):
    conn = get_conn()
    try:
        conn.execute(
            "DELETE FROM enrollments WHERE student_id=? AND course_id=?",
            (student_id, course_id),
        )
        conn.commit()
    finally:
        conn.close()
    print("Baja de curso exitosa")   # log inservible


# ---------------------------------------------------------------
# VERSIÓN DESPUÉS (trazable, atribuible, con integridad)
# ---------------------------------------------------------------
def _now_utc_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def drop_course(student_id, course_id, ip, user_agent, session_id):
    correlation_id = str(uuid.uuid4())
    ts = _now_utc_iso()

    # 1) Intento (antes de ejecutar)
    log_event("DROP_COURSE_ATTEMPT", student_id, course_id, ip, user_agent,
              session_id, correlation_id, ts, result="PENDING")

    try:
        conn = get_conn()
        try:
            cur = conn.execute(
                "DELETE FROM enrollments WHERE student_id=? AND course_id=?",
                (student_id, course_id),
            )
            affected = cur.rowcount
            conn.commit()
        finally:
            conn.close()

        if affected == 0:
            log_event("DROP_COURSE", student_id, course_id, ip, user_agent,
                      session_id, correlation_id, ts, result="NOT_ENROLLED")
            return {"ok": False, "reason": "NOT_ENROLLED", "correlation_id": correlation_id}

        log_event("DROP_COURSE", student_id, course_id, ip, user_agent,
                  session_id, correlation_id, ts, result="SUCCESS")
        return {"ok": True, "correlation_id": correlation_id}

    except Exception as e:
        log_event("DROP_COURSE", student_id, course_id, ip, user_agent,
                  session_id, correlation_id, ts, result="ERROR", reason=str(e))
        raise
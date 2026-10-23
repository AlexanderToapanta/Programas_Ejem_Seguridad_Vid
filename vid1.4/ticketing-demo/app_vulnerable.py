from flask import Flask, request, jsonify
import sqlite3
import uuid

app = Flask(__name__)
DB = "asientos.db"


def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS asientos (
            id INTEGER PRIMARY KEY,
            estado TEXT NOT NULL DEFAULT 'disponible',
            bloqueado_por TEXT
        )
    """)
    cur.execute("DELETE FROM asientos")
    for i in range(1, 11):
        cur.execute("INSERT INTO asientos (id, estado) VALUES (?, 'disponible')", (i,))
    con.commit()
    con.close()


def generar_token(id_usuario, id_asiento):
    return str(uuid.uuid4())


@app.route('/api/bloquear-asiento', methods=['POST'])
def bloquear_asiento():
    datos = request.get_json()
    id_asiento = datos.get('id_asiento')
    id_usuario = datos.get('id_usuario')

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("SELECT * FROM asientos WHERE id = ?", (id_asiento,))
    asiento = cur.fetchone()

    if asiento is None:
        con.close()
        return jsonify({"error": "asiento no existe"}), 404

    if asiento[1] == 'disponible':
        cur.execute(
            "UPDATE asientos SET estado='bloqueado', bloqueado_por=? WHERE id=?",
            (id_usuario, id_asiento)
        )
        con.commit()
        con.close()
        return jsonify({"token": generar_token(id_usuario, id_asiento)})

    con.close()
    return jsonify({"error": "asiento no disponible"}), 409


@app.route('/api/asientos', methods=['GET'])
def listar_asientos():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT id, estado, bloqueado_por FROM asientos")
    filas = cur.fetchall()
    con.close()
    return jsonify([
        {"id": f[0], "estado": f[1], "bloqueado_por": f[2]} for f in filas
    ])


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
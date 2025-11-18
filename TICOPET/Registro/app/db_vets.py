import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "ticopet.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def ensure_vets_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS veterinarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            colegiado TEXT UNIQUE NOT NULL,
            cedula TEXT,
            especialidad TEXT,
            telefono TEXT,
            correo TEXT,
            direccion TEXT,
            observaciones TEXT,
            registrado_por TEXT,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def create_vet(
    nombre: str,
    colegiado: str,
    cedula: str | None,
    especialidad: str | None,
    telefono: str | None,
    correo: str | None,
    direccion: str | None,
    observaciones: str | None,
    registrado_por: str | None
) -> bool:
    ensure_vets_table()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO veterinarios
            (nombre, colegiado, cedula, especialidad, telefono, correo, direccion, observaciones, registrado_por)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (nombre, colegiado, cedula, especialidad, telefono, correo, direccion, observaciones, registrado_por))
        conn.commit()
        ok = True
    except sqlite3.IntegrityError:
        ok = False
    finally:
        conn.close()
    return ok

import sqlite3
from pathlib import Path

# Usamos el mismo archivo de BD que el resto de la app
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
    """
    Inserta un veterinario. Devuelve False si el N.º de colegiado ya existe.
    """
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

def vet_exists(colegiado: str) -> bool:
    """
    Devuelve True si ya existe un veterinario con ese N.º de colegiado.
    """
    ensure_vets_table()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM veterinarios WHERE colegiado = ? LIMIT 1", (colegiado,))
    row = cur.fetchone()
    conn.close()
    return row is not None

def get_vet_by_colegiado(colegiado: str):
    """
    Devuelve una tupla con los datos del veterinario si existe, o None si no.
    Orden de columnas:
    (id, nombre, colegiado, cedula, especialidad, telefono, correo,
     direccion, observaciones, registrado_por, creado_en)
    """
    ensure_vets_table()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, colegiado, cedula, especialidad, telefono, correo,
               direccion, observaciones, registrado_por, creado_en
        FROM veterinarios
        WHERE colegiado = ?
        LIMIT 1
    """, (colegiado,))
    row = cur.fetchone()
    conn.close()
    return row

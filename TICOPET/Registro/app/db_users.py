import sqlite3
from pathlib import Path

# Ruta a ticopet.db (en la raíz del proyecto)
DB_PATH = Path(__file__).resolve().parents[1] / "ticopet.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def ensure_users_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            nombre TEXT,
            correo TEXT,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_user(nombre: str, usuario: str, correo: str, password: str) -> bool:
    ensure_users_table()
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO usuarios (nombre, usuario, correo, password)
            VALUES (?, ?, ?, ?)
        """, (nombre, usuario, correo, password))
        conn.commit()
        ok = True
    except sqlite3.IntegrityError:
        ok = False  # usuario duplicado
    finally:
        conn.close()
    return ok

def validate_user(usuario: str, password: str) -> bool:
    ensure_users_table()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 1 FROM usuarios
        WHERE usuario = ? AND password = ?
        LIMIT 1
    """, (usuario, password))
    row = cur.fetchone()
    conn.close()
    return row is not None
if __name__ == "__main__":
    print("✅ Commit de prueba vinculado a Azure Boards AB#13")

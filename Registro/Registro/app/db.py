import os
import sqlite3
from typing import Dict, Any

# Base de datos en la raíz del proyecto: ticopet.db
DB_FILE = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "ticopet.db"))

def init_db() -> None:
    """Crea la tabla usuarios si no existe."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rol TEXT NOT NULL CHECK (rol IN ('Owner','Veterinario','Recepcion','Admin')),
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            identificacion TEXT,
            email TEXT NOT NULL UNIQUE,
            telefono TEXT NOT NULL,
            direccion TEXT,
            password_hash BLOB NOT NULL,
            salt BLOB NOT NULL,
            terms_accepted INTEGER NOT NULL CHECK (terms_accepted IN (0,1)),
            marketing_opt_in INTEGER NOT NULL CHECK (marketing_opt_in IN (0,1)),
            whatsapp_opt_in INTEGER NOT NULL CHECK (whatsapp_opt_in IN (0,1)),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

def email_exists(email: str) -> bool:
    """True si el correo ya está registrado (case-insensitive)."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM usuarios WHERE lower(email)=lower(?) LIMIT 1", (email.strip(),))
    row = cur.fetchone()
    conn.close()
    return row is not None

def insert_user(data: Dict[str, Any]) -> int:
    """Inserta un usuario y devuelve su id."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO usuarios (
            rol, nombre, apellidos, identificacion, email, telefono, direccion,
            password_hash, salt, terms_accepted, marketing_opt_in, whatsapp_opt_in,
            created_at, updated_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            data["rol"],
            data["nombre"],
            data["apellidos"],
            data.get("identificacion"),
            data["email"],
            data["telefono"],
            data.get("direccion"),
            data["password_hash"],
            data["salt"],
            1 if data.get("terms_accepted") else 0,
            1 if data.get("marketing_opt_in") else 0,
            1 if data.get("whatsapp_opt_in") else 0,
            data["created_at"],
            data["updated_at"],
        ),
    )
    user_id = cur.lastrowid
    conn.commit()
    conn.close()
    return user_id

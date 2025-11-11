import sqlite3
from pathlib import Path

# Mismo archivo de base de datos que usas para usuarios
DB_PATH = Path(__file__).resolve().parents[1] / "ticopet.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def ensure_pets_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especie TEXT NOT NULL,
            raza TEXT,
            sexo TEXT,
            edad REAL,
            peso REAL,
            color TEXT,
            dueno TEXT NOT NULL,
            contacto TEXT,
            observaciones TEXT,
            registrado_por TEXT,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def create_pet(
    nombre: str,
    especie: str,
    raza: str,
    sexo: str,
    edad: str,
    peso: str,
    color: str,
    dueno: str,
    contacto: str,
    observaciones: str,
    registrado_por: str | None
) -> bool:
    """
    Inserta una mascota en la tabla.
    Devuelve True si todo va bien.
    """

    ensure_pets_table()
    conn = get_connection()
    cur = conn.cursor()

    # Intentamos convertir edad/peso a número, si no se puede los dejamos como NULL
    def to_float(value: str):
        try:
            return float(value.replace(",", "."))
        except (ValueError, AttributeError):
            return None

    edad_val = to_float(edad)
    peso_val = to_float(peso)

    cur.execute("""
        INSERT INTO mascotas
        (nombre, especie, raza, sexo, edad, peso, color,
         dueno, contacto, observaciones, registrado_por)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nombre,
        especie,
        raza or None,
        sexo or None,
        edad_val,
        peso_val,
        color or None,
        dueno,
        contacto or None,
        observaciones or None,
        registrado_por
    ))

    conn.commit()
    conn.close()
    return True

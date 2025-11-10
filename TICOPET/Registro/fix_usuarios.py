import sqlite3

conn = sqlite3.connect("ticopet.db")
cur = conn.cursor()

# Elimina la tabla vieja si existe
cur.execute("DROP TABLE IF EXISTS usuarios")

conn.commit()
conn.close()

print("Tabla 'usuarios' eliminada. Se creará con el nuevo esquema al registrar un usuario.")

import sqlite3

conn = sqlite3.connect("ticopet.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS mascotas")
conn.commit()
conn.close()

print("Tabla 'mascotas' eliminada. Se recreará con el nuevo esquema al guardar una mascota.")

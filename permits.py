import sqlite3

conn = sqlite3.connect("dados.sqlite")

cursor = conn.cursor()
ins = """
    update usuarios set usr_role = 'operador' where id_usr = 2;
"""
cursor.execute(ins)
conn.commit()
conn.close()
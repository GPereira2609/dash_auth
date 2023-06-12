import sqlite3

conn = sqlite3.connect("dados.sqlite")

cursor = conn.cursor()
# ins = """
#     update usuarios set usr_role = 'aprop_admin' where id_usr = 3;
# """

ins = """
    delete from usuarios where id_usr = 3;
"""

cursor.execute(ins)
conn.commit()
conn.close()
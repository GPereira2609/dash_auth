import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

conn = sqlite3.connect("dados.sqlite")

cursor = conn.cursor()
# ins = """
#     update usuarios set usr_role = 'aprop_admin' where id_usr = 3;
# """¨
senha = generate_password_hash("123", method="SHA256")
instructions = [
    f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('aprop_operador', '{senha}', 'teste@gmail.com', 'aprop_operador');",
    f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('aprop_admin', '{senha}', 'teste1@gmail.com', 'aprop_admin');",
    f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('lab_pcp', '{senha}', 'teste2@gmail.com', 'lab_pcp');",
    f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('lab_sgs', '{senha}', 'teste3@gmail.com', 'lab_sgs');",
    f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('gabriel.pereira', '{senha}', 'gabriel.pereira@gmail.com', 'aprop_admin');",
    f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('airon.nobre', '{senha}', 'airon.nobre@vale-verde.com', 'aprop_admin');",
    f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('teste_sgs', '{senha}', 'teste.sgs@geosol.com', 'lab_sgs');"
]

for ins in instructions:
    cursor.execute(ins)
    conn.commit()
conn.close()
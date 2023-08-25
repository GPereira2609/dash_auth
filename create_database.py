from sqlalchemy import Table, create_engine, text
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session

import sqlite3
import os 

conn = sqlite3.connect("dados.sqlite")
engine = create_engine('sqlite:///dados.sqlite')
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "usuarios"

    id_usr = db.Column(db.Integer, primary_key=True)
    nm_usr = db.Column(db.String(60), unique=True, nullable=False)
    email_usr = db.Column(db.String(60), nullable=False)
    pwd_usr = db.Column(db.String(60), nullable=False)
    usr_role = db.Column(db.String(60))

Users_table = Table('usuarios', User.metadata)

def criar_tabela_usuarios():
    User.metadata.create_all(engine)
criar_tabela_usuarios()

# import pandas as pd
# c = conn.cursor()
# df = pd.read_sql('select * from usuarios', conn)
# print(df)

with Session(engine) as session:
    user = session.get(User, 1)
    print(f"{user.id_usr} -> {user.nm_usr}")

# with Session(engine) as session:
#     # user = session.query(User, User.nm_usr).filter_by(User.nm_usr=="gabriel.pereira")
#     rst = session.query(User).filter(User.nm_usr==f"'{text('gabriel.pereira')}'")
#     user = rst[0]
#     print(user.pwd_usr) 


import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

# conn = sqlite3.connect("dados.sqlite")

# cursor = conn.cursor()
# # ins = """
# #     update usuarios set usr_role = 'aprop_admin' where id_usr = 3;
# # """¨
# senha = generate_password_hash("123", method="SHA256")
# instructions = [
#     f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('aprop_operador', '{senha}', 'teste@gmail.com', 'aprop_operador');",
#     f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('aprop_admin', '{senha}', 'teste1@gmail.com', 'aprop_admin');",
#     f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('lab_pcp', '{senha}', 'teste2@gmail.com', 'lab_pcp');",
#     f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('lab_sgs', '{senha}', 'teste3@gmail.com', 'lab_sgs');",
#     f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('gabriel.pereira', '{senha}', 'gabriel.pereira@gmail.com', 'aprop_admin');",
#     f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('airon.nobre', '{senha}', 'airon.nobre@vale-verde.com', 'aprop_admin');",
#     f"INSERT INTO usuarios (nm_usr, pwd_usr, email_usr, usr_role) VALUES ('teste_sgs', '{senha}', 'teste.sgs@geosol.com', 'lab_sgs');"
# ]

# for ins in instructions:
#     cursor.execute(ins)
#     conn.commit()
# conn.close()
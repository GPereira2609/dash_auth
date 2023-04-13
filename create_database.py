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
    email_usr = db.Column(db.String(60), unique=True, nullable=False)
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
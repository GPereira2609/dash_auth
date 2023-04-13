from dash import Dash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import dash_bootstrap_components as dbc
import sqlite3
from sqlalchemy import create_engine, Table
import os
import configparser

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

app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
app.config.suppress_callback_exceptions = True
server = app.server
server.config.update(
    SECRET_KEY = os.urandom(12),
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dados.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db.init_app(server)

class User(UserMixin, User):
    def get_id(self):
        return str(self.id_usr)
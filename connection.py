import sqlalchemy
import pyodbc
import pandas as pd

from sqlalchemy.orm import sessionmaker, declarative_base, relationship, backref
from sqlalchemy import text, Column, Integer, Float, String, ForeignKey, Date, Time, DateTime, create_engine
from urllib.parse import quote_plus
from sqlalchemy.engine import url
from sqlalchemy.engine.url import *

conn_url = URL.create(
    'mssql+pyodbc',
    username='sa',
    password='adm@123',
    host='192.168.1.8',
    port='1433',
    database='db_SistemaApropriaçãoMVV',
    query = dict(driver="SQL Server")
)

engine = create_engine(conn_url)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

conn = engine.connect()
import sqlalchemy
import pyodbc
import pandas as pd

from pandas import DataFrame, read_sql
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import  create_engine
from sqlalchemy.engine.url import *
from conn_ip import *

conn_url_lab = URL.create(
    "mssql+pyodbc",
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database="PCP_PLANTA",
    query=dict(driver="SQL Server")
)

engine = create_engine(conn_url_lab)
conn = engine.connect()


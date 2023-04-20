from connection import *
from pandas import DataFrame, read_sql

def popular_dropdown_processo_consultar_paradas():
    ins = 'select Producao from tbl_Paradas'
    df = DataFrame(read_sql(ins, conn))
    arr = []

    for i in df.drop_duplicates().values.tolist():
        arr.append(i[0])

    return arr

def popular_dropdown_sistema_consultar_paradas(value):
    ins = f"select Sistema from tbl_Paradas where Producao = '{value}'"
    df = DataFrame(read_sql(ins, conn))
    arr = []

    for i in df.drop_duplicates().values.tolist():
        arr.append(i[0])

    return arr


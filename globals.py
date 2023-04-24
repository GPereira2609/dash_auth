from connection import *
from pandas import DataFrame, read_sql

def popular_dropdown_processo_consultar_paradas():
    ins = 'select Producao from tbl_Paradas'
    df = DataFrame(read_sql(ins, conn))
    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_dropdown_sistema_consultar_paradas(value):
    ins = f"select Sistema from tbl_Paradas where Producao = '{value}'"
    df = DataFrame(read_sql(ins, conn))
    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_dropdown_equipamento_consultar_paradas(value_processo, value_sistema):
    ins = f"select Equipamento from tbl_Paradas where Producao = '{value_processo}' and Sistema = '{value_sistema}'" 
    df = DataFrame(read_sql(ins, conn))
    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr 

def menor_data_inicio():
    ins = "select min(DataInicio) from tbl_Paradas"
    df = DataFrame(read_sql(ins, conn))
    datetime = df.values[0][0]
    date = str(datetime)[:10]
    return str(date)
    # year, month, day = date.split("-")
    
    # return {
    #     "dia": int(day),
    #     "mes": int(month),
    #     "ano": int(year)
    # }

def menor_data_fim():
    ins = "select min(DataFim) from tbl_Paradas"
    df = DataFrame(read_sql(ins, conn))
    datetime = df.values[0][0]
    date = str(datetime)[:10]
    return str(date)
    # year, month, day = date.split("-")

    # return {
    #     "dia": int(day),
    #     "mes": int(month),
    #     "ano": int(year)
    # }

def retornar_todas_colunas_sem_id_e_datas():
    ins = 'select Validade, Producao, Sistema, Equipamento, EqpGerador, TipoCodigo, GrupoCodigo, CodigoFalha, Turno, CausaAparente, Operador, Observacao, Componente, ModoFalha, Apropriador from tbl_Paradas'
    df = DataFrame(read_sql(ins, conn))
    colunas = df.columns
    return colunas

def retornar_todas_colunas_sem_id_e_datas_por_id(id):
    ins = f'select Validade, Producao, Sistema, Equipamento, EqpGerador, TipoCodigo, GrupoCodigo, CodigoFalha, Turno, CausaAparente, Operador, Observacao, Componente, ModoFalha, Apropriador from tbl_Paradas where Id = {id}'
    df = DataFrame(read_sql(ins, conn))
    return df

def popular_dropdown_sistema_consultar_paradas_inicial():
    try:
        ins = 'select Sistema from tbl_Paradas'
        df = DataFrame(read_sql(ins, conn))
        arr = []

        for i in df.drop_duplicates().values.tolist():
            if i[0] != "Null":
                arr.append(i[0])

        return arr
    except:
        return []
from connection import *
from pandas import DataFrame, read_sql

def popular_dropdown_processo_consultar_paradas():
    ins = 'select Processo from tbl_Processos'
    df = DataFrame(read_sql(ins, conn))
    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_dropdown_sistema_consultar_paradas(value):
    ins = f"select Sistema from tbl_Sistemas where Processo = '{value}'"
    df = DataFrame(read_sql(ins, conn))
    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_dropdown_equipamento_consultar_paradas(value_processo, value_sistema):
    ins = f"select Equipamento from tbl_Equipamento where Processo = '{value_processo}' and Sistema = '{value_sistema}'" 
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

def dividir_parada_func(id, nova_hora):
    try:
        ins = f"select * from tbl_Paradas where id = {id}"
        df = DataFrame(read_sql(ins, conn))
        if df["DataFim"][0] != "Null":
            data_tempo_fim = df["DataFim"][0]
            data_fim = str(data_tempo_fim)[:10]

            proc = df["Producao"][0]
            sist = df["Sistema"][0]
            equip = df["Equipamento"][0]
            turno = df["Turno"][0]
            aprop = df["Apropriador"][0]

            ins1 = f"update tbl_Paradas set DataFim = convert(Datetime, '{data_fim} {nova_hora}') where Id = {id}"
            ins2 =  f"insert into tbl_Paradas (Producao, Sistema, Equipamento, Turno, Apropriador, DataInicio, DataFim) values ('{proc}', '{sist}', '{equip}', '{turno}', '{aprop}', convert(Datetime, '{data_fim} {nova_hora}'), convert(Datetime, '{data_tempo_fim}'))"
        elif df["DataFim"][0] == "Null":
            proc = df["Producao"][0]
            sist = df["Sistema"][0]
            equip = df["Equipamento"][0]
            turno = df["Turno"][0]
            aprop = df["Apropriador"][0]

            data_e_tempo_inicio = df["DataInicio"][0]
            data_inicio = data_e_tempo_inicio[:10]

            ins1 = f"update tbl_Paradas set DataFim = convert(Datetime, '{data_inicio} {nova_hora}') where Id = {id}"
            ins2 =  f"insert into tbl_Paradas (Producao, Sistema, Equipamento, Turno, Apropriador, DataInicio) values ('{proc}', '{sist}', '{equip}', '{turno}', '{aprop}', convert(Datetime, '{data_inicio} {nova_hora}'))"

        conn.execute(text(ins1))
        conn.execute(text(ins2))
        conn.commit()

        return "Divisão realizada com sucesso"
    except:
        return "Erro: dados não alterados"

def popular_dropdown_gerador_atualizar_parada():
    ins = f"select Equipamento from tbl_Equipamento"
    df_equip = DataFrame(read_sql(ins, conn))

    arr = []

    for i in df_equip.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr 

def popular_dropdown_tipo_de_codigo_atualizar_parada():
    ins = f"select [Tipo de Código] from tbl_TipoDeCódigo"
    df_tipo_de_codigo = DataFrame(read_sql(ins, conn))

    arr = []

    for i in df_tipo_de_codigo.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_dropdown_processo_atualizar_parada():
    ins = 'select Processo from tbl_Processos'
    df = DataFrame(read_sql(ins, conn))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_dropdown_sistema_atualizar_parada():
    ins = 'select Sistema from tbl_Sistemas'
    df = DataFrame(read_sql(ins, conn))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_dropdown_equipamento_atualizar_parada():
    ins = 'select Equipamento from tbl_Equipamento'
    df = DataFrame(read_sql(ins, conn))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def dropdown_turno_atualizar_paradas():
    ins = 'select Turno from tcl_turno'
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != 'Null':
            arr.append(i[0])

    return arr

def popular_processo_modal_adicionar_campo():
    ins = "select Processo from tbl_Equipamento"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_sistema_modal_adicionar_campo():
    ins = f"select Sistema from tbl_Equipamento"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_grupo_equipamento_modal_adicionar_campo():
    ins = f"select [Grupo de Equipamentos] from tbl_Equipamento"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_grupo_codigo_modal_adicionar_campo():
    ins = "select [Grupo de Código] from tbl_CódigoDasFalhas" 
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_codigo_falha_modal_adicionar_campo():
    ins = "select CodigoFalha from tbl_CausaAparente"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_grupo_equipamentos_modal_adicionar_campo():
    ins = "select [Grupo de Equipamentos] from tbl_Componente"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_causa_aparente_modaladicionar():
    ins = "select CodigoFalha from tbl_CausaAparente"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_componente_modaladicionar():
    ins = "select [Grupo de Equipamentos] from tbl_Componente"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_turnos():
    ins = "select Turno from tcl_turno"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_tipo_codigo_consultar_paradas():
    ins = "select [Tipo de Código] from tbl_TipoDeCódigo"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_componente_consultar_parada():
    ins = "select Componente from tbl_Componente"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_gerador_aprop_paradas():
    ins = "select Equipamento from tbl_Equipamento"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_tipocodigo_aprop_paradas():
    ins = "select [Tipo de Código] from tbl_TipoDeCódigo"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_aprop_paradas_processo():
    ins = "select Processo from tbl_Processos"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_aprop_paradas_sistema():
    ins = f"select Sistema from tbl_Sistemas"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_aprop_paradas_equip():
    ins = "select Equipamento from tbl_Equipamento"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr

def popular_aprop_paradas_turno():
    ins = "select Turno from tcl_Turno"
    df = DataFrame(read_sql(ins, engine.connect()))

    arr = []

    for i in df.drop_duplicates().values.tolist():
        if i[0] != "Null":
            arr.append(i[0])

    return arr
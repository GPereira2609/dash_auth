from app import *
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table, Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import logout_user
from sqlalchemy import text

from globals import *

card_style = {
    'width': '500px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'column'
}

card_style2= {
    'width': '1120px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center',
    'display': 'flex',
    'flex-direction': 'column'
}


def render_layout(user):
    username = user.nm_usr
    
    layout = html.Div([
            dbc.Row([
                html.Div([
                    html.Div([
                    dcc.Location(id="consultar_paradas_base_url"),
                    html.H3(username.replace("'", ""), style={"color": "white"}),
                    
                ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'height': "100%"}),

                    html.Div([
                        dbc.Nav([
                            dbc.NavLink("Home", href="/home", active="exact"),
                            dbc.NavLink("Consultar paradas", href="/consultar_paradas", active="exact"),
                            dbc.NavLink("Apropriar paradas", href="/aprop_paradas", active="exact"),
                            dbc.NavLink("Consultar turno", href="/consultar_turno", active="exact"),
                            dbc.NavLink("Apropriação turno", href="/aprop_turno", active="exact"),
                            dbc.NavLink("Registrar usuário", href="/register", active="exact")
                        ], pills=True, vertical=False, id='nav')
                    ], style={"height": "100%", 'display': 'flex', 'flex-direction': 'column'}),

                    html.Div([
                        html.Img(src=app.get_asset_url('f2711217-e0a9-4a63-a24c-3c969b7ce090.png'), height=75, width=194)
                    ])
                ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}),
                
            ], style={"height": '15%', 'width': '105vw', 'display': 'block', 'justify-content': 'space-evenly', 'background-color': '#298753'}),

            dbc.Row([   
                html.Div([
                    
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                html.Legend("Processo/equipamento"),
                                dbc.Row([
                                    dbc.Label("Processo: "),
                                    dcc.Dropdown(options=popular_dropdown_processo_consultar_paradas(), id="dropdown_processo_consultar_paradas", value=popular_dropdown_processo_consultar_paradas()[0])
                            ]),
                                dbc.Row([
                                    dbc.Label("Sistema: "),
                                    dcc.Dropdown(options=[], id="dropdown_sistema_consultar_paradas")
                            ]),
                                dbc.Row([
                                    dbc.Label("Equipamento: "),
                                    dcc.Dropdown(options=[], id="dropdown_equipamento_consultar_paradas")
                            ]),
                            ], style=card_style),
                            
                            ]),

                        dbc.Col([
                            dbc.Card([
                                html.Legend("Período"),
                                dbc.Row([
                                    dbc.Label("Início: "),
                                    dcc.DatePickerSingle(display_format="DD/MM/YYYY", id="data_inicio_consultar_paradas", min_date_allowed=menor_data_inicio())
                            ]),

                                dbc.Row([
                                    dbc.Label("Fim: "),
                                    dcc.DatePickerSingle(display_format="DD/MM/YYYY", id="data_fim_consultar_paradas", min_date_allowed=menor_data_fim())
                            ]),

                                dbc.Row([
                                    dbc.Button("Consultar", id="botao_consulta_paradas", style={"margin": "10px", 'width': '100px'})
                                ])
                            ], style=card_style),
                            
                        ])
                        ], style={"padding-top": "25px"}),

                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    html.Legend("Dados"),
                                    dbc.Row([
                                        dbc.Label("Dados"),
                                        dash_table.DataTable(id="tabela_dados", data=[{}], row_selectable="single", selected_rows=[])
                                    ])
                                ], style=card_style2)
                            ])
                        ], style={"padding-top": "25px"}),

                        dbc.Row([
                            dbc.Col([
                                html.H4("ID selecionado: ", id="marcador_id_consultar_paradas"),
                                dbc.Button("Atualizar", id="atualizar_consultar_paradas", style={"margin": "10px", 'width': '100px'}),
                                dbc.Modal([
                                    dbc.ModalHeader(dbc.ModalTitle("Atualizar")),
                                    dbc.ModalBody([
                                        html.Div([
                                            dcc.Dropdown(id="dropdown_modal_atualizar", options=retornar_todas_colunas_sem_id_e_datas(), style={"margin": '5px', "padding": "5px"}, value=None),
                                            dcc.Input(id="input_modal_atualizar", type="text"),
                                            html.H4(id="msg_modal_atualizar")
                                        ], style={"display": "flex", "flex-direction": "column", "justify-content": "center"})
                                        
                                    ]),
                                    dbc.ModalFooter([
                                        dbc.Button("Fechar", id="fechar_modal"),
                                        dbc.Button("Atualizar", id="atualizar_modal")
                                    ])
                                ], id="modal_atualizar", size="lg", is_open=False),
                                dbc.Button("Excluir", id="excluir_consultar_paradas", style={"margin": "10px", 'width': '100px'}),
                                html.H4(id="gateway_instrucoes"),
                                dbc.Button("Dividir", id="dividir_consultar_paradas", style={"margin": "10px", 'width': '100px'}),
                                dbc.Button("Copiar", id="copiar_consultar_paradas", style={"margin": "10px", 'width': '100px'}),
                                html.H4(id="gateway_instrucoes2")
                            ])
                        ])
                        

                    ], style={"display": "flex", "flex-direction": "column", "justify-content": "center", "margin-left": "10px"})


            ], style={"height": '85%', 'width': '100%', 'background-color': "white"})
        ], style={'background-color': "white", 'height': '100vh', 'width': '100vw', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'width': '100vw'})
        
    return layout

@app.callback(
    Output("dropdown_sistema_consultar_paradas", "options"),
    Input("dropdown_processo_consultar_paradas", "value")
)
def popular_dropdown_sistemas(value):
    if value is None:
        raise PreventUpdate
    if value is not None:
        return popular_dropdown_sistema_consultar_paradas(value)

@app.callback(
    Output("dropdown_equipamento_consultar_paradas", "options"),
    Input("dropdown_processo_consultar_paradas", "value"),
    Input("dropdown_sistema_consultar_paradas", "value")
)
def popular_dropdown_equipamento(value_processo, value_sistema):
    if value_processo is None:
        raise PreventUpdate
    if value_sistema is None:
        raise PreventUpdate
    return popular_dropdown_equipamento_consultar_paradas(value_processo, value_sistema) 

@app.callback(
    Output("tabela_dados", "data"),
    Output("tabela_dados", "columns"),
    Input("botao_consulta_paradas", "n_clicks"),
    [
        State("dropdown_sistema_consultar_paradas", "value"),
        State("dropdown_processo_consultar_paradas", "value"),
        State("dropdown_equipamento_consultar_paradas", "value"),
        State("data_inicio_consultar_paradas", "date"),
        State("data_fim_consultar_paradas", "date")   
    ]
)
def consultar_paradas(n, sist, proc, equip, dt_inicio, dt_fim):
    if (sist or proc or equip or dt_inicio or dt_fim) is None:
        raise PreventUpdate 
    if n is None:
        raise PreventUpdate
    if n is not None:
        ins = f"select Id, Validade, Producao, Sistema, Equipamento, DataInicio, DataFim, Duracao, EqpGerador from tbl_Paradas where Sistema = '{sist}' and Producao = '{proc}' and Equipamento = '{equip}' and DataInicio >= convert(Datetime, '{dt_inicio}') and DataFim <= convert(Datetime, '{dt_fim}')"
        df = DataFrame(read_sql(ins, conn))
        cols = []
        for col in df.columns:
            cols.append({"name": str(col), "id": str(col)})

        values = df.to_dict(orient="records")

        return [values, cols]

@app.callback(
    Output("marcador_id_consultar_paradas", "children"),
    Input("tabela_dados", "selected_rows"),
    State("tabela_dados", "data")
)
def mostrar_id_consultar_paradas(rows, tabela):
    if len(rows) != 0:
        data = str(tabela[rows[0]]["Id"])
        return f"ID selecionado: {data}"

@app.callback(
    Output("gateway_instrucoes", "children"),
    Input("excluir_consultar_paradas", "n_clicks"),
    State("tabela_dados", "selected_rows"),
    State("tabela_dados", "data")
)
def excluir_consultar_paradas(n, rows, tabela):
    if n is None:
        raise PreventUpdate
    if n is not None:
        if len(rows) != 0:
            id = str(tabela[rows[0]]["Id"])
            ins = f"delete from tbl_Paradas where Id = {int(id)}"
            with engine.connect() as conn:
                    conn.execute(text(ins))
                    conn.commit()
                    conn.close()
            return ''

@app.callback(
    Output("gateway_instrucoes2", "children"),
    Input("copiar_consultar_paradas", "n_clicks"),
    State("tabela_dados", "selected_rows"),
    State("tabela_dados", "data")
)
def copiar_consultar_paradas(n, rows, tabela):
    if n is None:
        raise PreventUpdate
    if n is not None:
        if len(rows) != 0:

            id = str(tabela[rows[0]]["Id"])

            ins = f"insert into tbl_Paradas(Validade, Producao, Sistema, Equipamento, DataInicio, DataFim, EqpGerador, TipoCodigo, GrupoCodigo, CodigoFalha, Turno, CausaAparente, Operador, Observacao, Componente, ModoFalha, Apropriador) select Validade, Producao, Sistema, Equipamento, DataInicio, DataFim, EqpGerador, TipoCodigo, GrupoCodigo, CodigoFalha, Turno, CausaAparente, Operador, Observacao, Componente, ModoFalha, Apropriador from tbl_Paradas where ID = {id}"
            

            with engine.connect() as conn:
                conn.execute(text(ins))
                conn.commit()
                conn.close()
            return ''
      
@app.callback(
    Output("modal_atualizar", "is_open"),
    [
        Input("atualizar_consultar_paradas", "n_clicks"),
        Input("fechar_modal", "n_clicks")
    ],
    State("modal_atualizar", "is_open")
)
def controlar_modal(n_abrir, n_fechar, n):
    if n_abrir or n_fechar:
        return not n
    return n

@app.callback(
    Output("input_modal_atualizar", "value"),
    Input("dropdown_modal_atualizar", "value"),
    State("tabela_dados", "selected_rows"),
    State("tabela_dados", "data")
)
def mostrar_input_id_atual(value, rows, tabela):
    if value is not None:
        id = tabela[rows[0]]["Id"]
        ins = f"select {value} from tbl_Paradas where Id = {int(id)}"
        df = DataFrame(read_sql(ins, conn))
        
        return df.values[0][0]

@app.callback(
    Output("msg_modal_atualizar", "children"),
    Input("atualizar_modal", "n_clicks"),
    State("modal_atualizar", "is_open"),
    State("dropdown_modal_atualizar", "value"),
    State("input_modal_atualizar", "value"),
    State("tabela_dados", "selected_rows"),
    State("tabela_dados", "data")
)
def atualizar_com_infos_modal(n, is_open, col_value, data_value, rows, tabela):
    if is_open:
        if n is None:
            raise PreventUpdate
        if n is not None:
            try:
                id = tabela[rows[0]]["Id"]
                ins = f"update tbl_Paradas set {col_value} = '{data_value}' where Id = {int(id)}"
                with engine.connect() as conn:
                    conn.execute(text(ins))
                    conn.commit()
                    conn.close()
                return 'Dados atualizados'
            except:
                return 'Erro: os dados não foram alterados'
    if not is_open:
        return ''
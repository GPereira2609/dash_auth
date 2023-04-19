import dash_bootstrap_components as dbc

from dash import html, dcc

def render_layout(username):
    layout = dbc.Container([
        html.Div([
        html.Div([
            html.H1(username.replace("'", "")),
            html.Button("Logout", id="logout", style={'width': '100px'})
        ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-self': 'center'}),
        html.Hr(),
        ]),
        
        dbc.Nav([
            html.Div([
                dbc.NavLink("Consultar paradas", href="/consultar_paradas", active="exact"),
                dbc.NavLink("Apropriar paradas", href="/aprop_paradas", active="exact"),
                dbc.NavLink("Consultar turno", href="/consulatr_turno", active="exact"),
                dbc.NavLink("Apropriação turno", href="/aprop_turno", active="exact")
            ], style={'height': '50%'}),

            html.Div([], style={'height': '50%'})
        ], style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'space-evenly', 'padding-left': '0 !important'}, vertical=False, pills=True, id="nav")
    ])

    return layout


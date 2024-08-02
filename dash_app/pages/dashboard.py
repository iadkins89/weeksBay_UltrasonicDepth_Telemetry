from dash import dcc, html, register_page
import dash_table
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

register_page(
    __name__,
    top_nav=True,
    path='/dashboard'
)

def layout():
    datums = ["MLLW", "MLW", "MSL", "MTL", "MHW", "MHHW", "STND"]

    return dbc.Container([
        dbc.Row([
            dbc.Col(dcc.DatePickerRange(
                id='graph-date-picker',
                start_date=datetime.today(),
                end_date=datetime.today() + timedelta(days=1),
                stay_open_on_select=True,
                style={"margin-left": "15px"}
            )),
            dbc.Col(),
            dbc.Col(
                html.Div(
                    dcc.Dropdown(
                        id='table-dropdown',
                        options=datums,
                        value=datums[0],
                        style={'width': '100%'},
                    ),
                    style={'width': '90%', 'maxHeight': '100px'},
                ),
                width=5
            )
        ], style={'paddingTop': '5px'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='depth-graph'), width=8),
            dbc.Col(html.Div([html.Div([
                html.H4("Most Recent Tidal Recording", style={
                    'marginBottom': '8px',
                    'textAlign': 'center',
                    'fontSize': '16px'
                }),
                html.Div(id='recent-tide-measurement', style={
                    'backgroundColor': 'white',
                    'color': '#34495E',
                    'height': '200px',
                    'width': '200px',
                    'overflowY': 'scroll',
                    'padding': '10px',
                    'border': '2px solid #137ea7',
                    'borderRadius': '10px',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'textAlign': 'center'
                })
            ])], style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'justifyContent': 'center',
                'textAlign': 'center'  # Center align text in the parent div
            }))
        ]),
        dbc.Row([
            dbc.Col(dash_table.DataTable(
                id='tide-table',
                columns=[
                    {'name': 'Time', 'id': 'time'},
                    {'name': 'Tide Level', 'id': 'tide_level'},
                    {'name': 'Predicted Tide Level', 'id': 'predicted_tide_level'}
                ],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
            ), width=12)
        ]),
        dbc.Row([
            dbc.Col(dbc.Form([
                dbc.Row([
                    dbc.Col(dbc.Input(id="csv-filename", placeholder="Enter CSV filename"), width=4),
                    dbc.Col(dcc.DatePickerRange(
                        id='date-picker-range',
                        start_date=datetime.today(),
                        end_date=datetime.today(),
                        stay_open_on_select=True,
                        style={'padding': '10px'}
                    ), width=4),
                    dbc.Col(dbc.Button("Download CSV", id="set-filename-btn", color="primary"), width=4)
                ], align='center')
            ]), width=12),
            dbc.Col(dcc.ConfirmDialog(
                id='confirm-dialog',
                message=''
            )),
            dbc.Col(dcc.Download(id="download-dataframe-csv"))
        ]),
    ])



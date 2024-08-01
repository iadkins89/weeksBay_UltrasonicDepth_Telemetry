from dash import dcc, html, register_page
import dash_bootstrap_components as dbc
from datetime import datetime
from dash_extensions import EventSource

register_page(
	__name__,
	top_nav=True,
	path='/dashboard'
)


def layout():
    datums = ["MLLW", "MLW", "MSL", "MTL", "MHW", "MHHW", "STND"]
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Form([
                dbc.Input(id="csv-filename", placeholder="Enter CSV filename"),
                dbc.Button("Download CSV", id="set-filename-btn", color="primary", className="mt-2"),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=datetime.today(),
                    end_date=datetime.today(),
                    stay_open_on_select=True,
                    style={"margin-left": "15px",
                           'padding': '10px'}
                ),
                dcc.ConfirmDialog(
                    id='confirm-dialog',
                    message=''
                ),
                dcc.Download(id="download-dataframe-csv")
            ]), width=5),
            dbc.Col(),
            dbc.Col(
                html.Div(
                    dcc.Dropdown(
                        id='table-dropdown',
                        options=datums,
                        value=datums[0],
                        style={'width': '100%'},
                    ),
                    style={'width': '90%', 'maxHeight': '100px', 'overflowY': 'scroll'},
                ),
                width=5
            )
        ]),
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
                    'border': '2px solid #2ECC71',
                    'borderRadius': '10px',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'textAlign': 'center'
                })
            ])],style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'textAlign': 'center'  # Center align text in the parent div
                })
            )
        ]),
        EventSource(id='eventsource', url='/eventsource')

    ])
	
    return layout
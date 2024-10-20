from dash import dash_table, dcc, html, register_page
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta
from server.models import most_recent_query
import dash_daq as daq

register_page(
    __name__,
    top_nav=True,
    path='/dashboard'
)

def layout():
    datums = ["NAVD88", "MLLW", "MLW", "MSL", "MTL", "MHW", "MHHW", "STND"]

    most_recent_data = most_recent_query()

    # Format the date and time for display
    if most_recent_data and most_recent_data.timestamp:
        timestamp_date = most_recent_data.timestamp.strftime('%Y-%m-%d')
        timestamp_time = most_recent_data.timestamp.strftime('%H:%M:%S')
    else:
        timestamp_date = ""
        timestamp_time = ""

    battery_level = most_recent_data.battery if most_recent_data and most_recent_data.battery else 0

    return dbc.Container([
        dbc.Row([
            dbc.Col(dcc.DatePickerRange(
                id='graph-date-picker',
                start_date=datetime.today(),
                end_date=datetime.today(),
                stay_open_on_select=True,
                minimum_nights=0,
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
            dbc.Col(dcc.Graph(id='depth-graph', config={
                'modeBarButtonsToRemove': [
                    'zoom2d', 'pan2d', 'select2d', 'lasso2d',
                    'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d',
                    'hoverClosestCartesian', 'hoverCompareCartesian',
                    'toggleSpikelines'
                ],
                'displaylogo': False
            }), width=8),

            dbc.Col(html.Div([
                html.H4("Most Recent Tidal Recording", style={
                    'marginBottom': '8px',
                    'textAlign': 'center',
                    'fontSize': '16px'
                }),
                html.Div([
                    html.Div(
                        f"{round(most_recent_data.tide, 2)} m" if most_recent_data and most_recent_data.tide else "",
                        style={
                            'fontSize': '24px',
                            'fontWeight': 'bold',
                        }),
                    html.Div(timestamp_date,
                             style={
                                 'fontSize': '14px',
                                 'marginTop': '8px'
                             }),
                    html.Div(timestamp_time,
                             style={
                                 'fontSize': '14px',
                                 'marginTop': '4px'
                             }
                             )
                ], style={
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
                }),

                # Add the gauge below the most recent tidal recording
                daq.Gauge(
                    id='battery-gauge',
                    showCurrentValue=True,
                    min=0,
                    max=100,
                    value=battery_level,  # Replace with actual data
                    label="Battery Level",
                    color={"gradient": True, "ranges": {"green": [50, 100], "yellow": [20, 50], "red": [0, 20]}},
                    style={'marginTop': '20px'}
                )
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'justifyContent': 'center',
                'textAlign': 'center'
            }))
        ]),

        dbc.Row([
            dbc.Col(dash_table.DataTable(
                id='tide-table',
                columns=[
                    {'name': 'Time', 'id': 'time'},
                    {'name': 'Tide Level (m)', 'id': 'tide_level'}
                ],
                page_size=7,
                page_current=0,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                page_action='custom'
            ), width=12)
        ]),

        dbc.Row([
            dbc.Col(dbc.Form([
                dbc.Row([
                    dbc.Col(dbc.Input(id="csv-filename", placeholder="Enter CSV filename"), width=4),
                    dbc.Col(dbc.Button("Download CSV", id="set-filename-btn", color="primary"), width=4)
                ], align='center')
            ]), width=12),
            dbc.Col(dcc.ConfirmDialog(
                id='confirm-dialog',
                message=''
            )),
            dbc.Col(dcc.Download(id="download-dataframe-csv"))
        ]),
        dbc.Row()
    ])



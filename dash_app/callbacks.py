from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
import json
from datetime import datetime
from server.models import query_data, save_data_to_csv

def register_callbacks(app):
    @app.callback(
        Output('depth-graph', 'figure'),
        [Input('eventsource', 'message'),
        Input('table-dropdown', 'value')]
    )
    def update_depth_graph(message, datum):
        if not message:
            return go.Figure()

        data = json.loads(message)

        timestamps = [d['timestamp'] for d in data]
        depth = [d['depth'] for d in data]

        return {
            'data': [go.Scatter(
                x=timestamps,
                y=depth,
                mode='lines+markers',
                name='Depth',
                marker={'color': 'mediumturquoise'},
                fill='tozeroy',  # This fills the area under the line
                fillcolor='rgba(72, 209, 204, 0.2)'  # Optional: to control the fill color and its transparency
            )],
            'layout': go.Layout(
                title='Weeks Bay Depth',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Depth (ft)', 'range': [0, 15]}
            )
        }

    @app.callback(
        Output('confirm-dialog', 'displayed'),
        Output('confirm-dialog', 'message'),
        Output('download-dataframe-csv', 'data'),
        [Input('set-filename-btn', 'n_clicks')],
        [State('date-picker-range', 'start_date'),
         State('date-picker-range', 'end_date'),
         State('csv-filename', 'value'),
         State('table-dropdown', 'value')]
    )
    def update_output(n_clicks, start_date, end_date, filename, sensor_name):
        if n_clicks is None:
            raise PreventUpdate
        else:
            if not start_date or not end_date or not filename:
                return True, 'Please provide a valid date range and filename.', None

            data = query_data(start_date, end_date, sensor_name)
            if not data:
                return True, 'No data found for the given date range.', None

            saved_csv_file = save_data_to_csv(data, f"{filename}.csv")
            return False, '', dict(content=saved_csv_file, filename=f"{filename}.csv")
        return False, '', None

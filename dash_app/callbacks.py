from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from server.models import date_query, save_data_to_csv, predictions

def register_callbacks(app):
    @app.callback(
        Output('depth-graph', 'figure'),
        [Input('graph-date-picker', 'start_date'),
        Input('graph-date-picker', 'end_date'),
        Input('table-dropdown', 'value')]
    )
    def update_depth_graph(start_date, end_date, datum):
        data = date_query(start_date,end_date)

        tide_predictions = predictions(start_date, end_date)
        timestamps = [d['timestamp'] for d in data]
        tide_level = [d['depth'] for d in data]
        pred_tide_levels = [prediction[1] for prediction in tide_predictions]

        return {
            'data': [go.Scatter(
                x=timestamps,
                y=tide_level,
                mode='lines+markers',
                name='Tide Level',
                marker={'color': 'mediumturquoise'},
                fill='tozeroy',  # This fills the area under the line
                fillcolor='rgba(72, 209, 204, 0.2)'  # Optional: to control the fill color and its transparency
            ),
            go.Scatter(
                x=[prediction[0] for prediction in tide_predictions],
                y=pred_tide_levels,
                mode='lines+markers',
                name='Predicted Tide Levels',
                marker={'color': 'orange'},
                line={'dash': 'dash', 'width': .01}
            )
        ],
            'layout': go.Layout(
                title='Weeks Bay Depth',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Tide Level (ft)', 'range': [-1, 7]}
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
    def update_output(n_clicks, start_date, end_date, filename, datum_name):
        if n_clicks is None:
            raise PreventUpdate
        else:
            print(start_date)
            if not start_date or not end_date or not filename:
                return True, 'Please provide a valid date range and filename.', None

            data = date_query(start_date, end_date)
            if not data:
                return True, 'No data found for the given date range.', None

            saved_csv_file = save_data_to_csv(data, datum_name, f"{filename}.csv")
            return False, '', dict(content=saved_csv_file, filename=f"{filename}.csv")
        return False, '', None

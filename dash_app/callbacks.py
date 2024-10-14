from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go
from server.models import date_query, save_data_to_csv, most_recent_query

def register_callbacks(app):
    @app.callback(
        Output('depth-graph', 'figure'),
        [Input('graph-date-picker', 'start_date'),
        Input('graph-date-picker', 'end_date'),
        Input('table-dropdown', 'value')]
    )
    def update_depth_graph(start_date, end_date, datum):
        data = date_query(start_date,end_date)

        timestamps = [d.timestamp for d in data]
        tide_level = [d.tide for d in data]

        return {
            'data': [go.Scatter(
                x=timestamps,
                y=tide_level,
                mode='lines+markers',
                name='Tide Level',
                marker={'color': 'mediumturquoise', 'size': 5},
            )
        ],
            'layout': go.Layout(
                title='Weeks Bay Tidal Observations',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Tide Level (m)', 'range': [0, 10]},
                legend=dict(
                    x=0,  # Position the legend at the top-left corner
                    y=1,
                    traceorder='normal'
                )
            )
        }
    @app.callback(
        Output('tide-table', 'data'),
        Output('tide-table', 'page_count'),
        [Input('graph-date-picker', 'start_date'),
         Input('graph-date-picker', 'end_date'),
         Input('table-dropdown', 'value'),
         Input('tide-table', 'page_current'),
         Input('tide-table', 'page_size')]
    )
    def update_table(start_date, end_date, datum, page_current, page_size):
        data = date_query(start_date, end_date)

        table_data = []
        for d in data:
            table_data.append({
                'time': d.timestamp,
                'tide_level': d.tide
            })

        start = page_current * page_size
        end = start + page_size
        page_count = len(table_data) // page_size + (len(table_data) % page_size > 0)
        return table_data[start:end], page_count

    @app.callback(
        Output('confirm-dialog', 'displayed'),
        Output('confirm-dialog', 'message'),
        Output('download-dataframe-csv', 'data'),
        [Input('set-filename-btn', 'n_clicks')],
        [State('graph-date-picker', 'start_date'),
         State('graph-date-picker', 'end_date'),
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

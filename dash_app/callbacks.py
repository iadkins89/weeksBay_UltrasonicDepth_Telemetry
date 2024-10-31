from dash import no_update, callback_context
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
        data = date_query(start_date, end_date)

        timestamps = [d.timestamp for d in data]
        tide_level = [d.tide for d in data]

        # Calculate dynamic range for y-axis if tide_level is not empty
        if tide_level:
            y_min = 0
            y_max = max(tide_level) + 0.25
        else:
            y_min, y_max = 0, 1  # Default range if there's no data

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
                xaxis={'title': 'Time'},
                yaxis={'title': 'Tide Level (m)', 'range': [y_min, y_max]},
                legend=dict(
                    x=0,  # Position the legend at the top-left corner
                    y=1,
                    traceorder='normal'
                ),
                margin=dict(l=40, r=10, t=10, b=45)
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
            if not start_date or not end_date or not filename:
                return True, 'Please provide a valid date range and filename.', None

            data = date_query(start_date, end_date)
            if not data:
                return True, 'No data found for the given date range.', None

            saved_csv_file = save_data_to_csv(data, datum_name, f"{filename}.csv")
            return False, '', dict(content=saved_csv_file, filename=f"{filename}.csv")
        return False, '', None

    # Callback to handle marker click and redirect
    @app.callback(
        Output('url', 'pathname'),
        Input('map-graph', 'clickData')
    )
    def redirect_on_click(clickData):
        if clickData:
            # Example: redirect to a page specific to this sensor's details
            return '/dashboard'  # or generate URL dynamically based on sensor information
        return no_update

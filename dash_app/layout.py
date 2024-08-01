import dash
from dash import html
from .navmenu import create_menu

def get_layout():
    layout = html.Div(
        [
            create_menu(),
            dash.page_container,
        ]
    )

    return layout

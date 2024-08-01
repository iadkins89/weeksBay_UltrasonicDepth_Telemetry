from dash import html
import dash_bootstrap_components as dbc


def create_menu():
    navmenu = dbc.Navbar(
        dbc.Container(
            [
                dbc.Row([
                    dbc.Col(html.Img(src='/assets/weeks-bay.png', style={'height': '100px'}), width='auto'),
                    dbc.Col(html.H1("Weeks Bay Tide", className="text-left", style={'color': '#154360'}), width='auto')
                ], align='center'),
                dbc.Nav(
                    [
                        dbc.NavLink("Home", active="exact", href="/"),
                        dbc.NavLink("Dashboard", active="exact", href="/dashboard"),
                        dbc.NavLink("About", active="exact", href="/about"),
                    ],
                    pills=True,
                ),
            ]
        ),
        class_name="custom-navbar"
    )

    return navmenu

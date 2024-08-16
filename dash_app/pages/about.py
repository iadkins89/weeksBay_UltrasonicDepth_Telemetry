from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    top_nav=True,
    path='/about'
)

def layout():
    layout = dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H1("About Us", style={"margin-top": "35px", "margin-left": "190px", "margin-right": "190px"}),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        "Welcome to the Weeks Bay Ultrasonic Depth Telemetry Project, a collaborative effort based in Fairhope, Alabama, "
                        "aimed at advancing our understanding of tidal dynamics in the Weeks Bay Reserve. This project is part of the ongoing "
                        "commitment by the University of South Alabama to leverage innovative technology for environmental monitoring and conservation. "
                        "Utilizing an ultrasonic sensor, our system measures real-time water (tide) levels and transmits the data via LoRaWAN (Long Range "
                        "Wide Area Network) technology, providing critical insights into the tidal patterns of this vital coastal region.",
                        className="lead",
                        style={"margin-left": "190px", "margin-right": "190px"}
                    ),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.H2("Our Mission", style={"margin-left": "190px", "margin-right": "190px"}),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        "Our mission is to contribute to the sustainability and preservation of Weeks Bay by providing accurate, real-time data on tidal movements. "
                        "By deploying state-of-the-art telemetry systems, we aim to:",
                        className="lead",
                        style={"margin-left": "190px", "margin-right": "190px"}
                    ),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Ul(
                        [
                            html.Li("Continuously monitor water levels to understand tidal behaviors and their impact on the ecosystem.", style={"margin-left": "190px", "margin-right": "190px"}),
                            html.Li("Support conservation efforts by offering reliable data to researchers and environmental agencies.", style={"margin-left": "190px", "margin-right": "190px"}),
                            html.Li("Enhance public awareness and education about the importance of coastal ecosystems through accessible and transparent data sharing.", style={"margin-left": "190px", "margin-right": "190px"}),
                        ]
                    ),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.H2("Our Technology", style={"margin-left": "190px", "margin-right": "190px"}),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        "Our project employs the following advanced technologies to ensure precise and reliable data collection:",
                        className="lead",
                        style={"margin-left": "190px", "margin-right": "190px"}
                    ),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.Ul(
                        [
                            html.Li("Ultrasonic Sensor: Accurately measures the distance from the sensor to the water surface, allowing us to monitor tide levels with high precision.", style={"margin-left": "190px", "margin-right": "190px"}),
                            html.Li("LoRaWAN Communication: Enables long-range, low-power transmission of data, ensuring that information is relayed in real-time even from remote locations within the reserve.", style={"margin-left": "190px", "margin-right": "190px"}),
                            html.Li("Real-Time Data: Provides instant access to water level information, facilitating timely decision-making for environmental management.", style={"margin-left": "190px", "margin-right": "190px"}),
                        ]
                    ),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.H2("Get Involved", style={"margin-left": "190px", "margin-right": "190px"}),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        "We welcome students, researchers, and community members who are passionate about coastal conservation and technology to join our project. "
                        "Whether your interest lies in fieldwork, data analysis, or technological innovation, there are numerous opportunities to contribute to our mission.",
                        className="lead",
                        style={"margin-left": "190px", "margin-right": "190px"}
                    ),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.H2("Contact Us", style={"margin-left": "190px", "margin-right": "190px"}),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        "For more information about our project, collaborations, or any inquiries, please feel free to reach out to us at:",
                        className="lead",
                        style={"margin-left": "190px", "margin-right": "190px"}
                    ),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        [
                            "Email: ",
                            html.A("iea2021@jagmail.southalabama.edu", href="mailto:iea2021@jagmail.southalabama.edu"),
                        ],
                        className="lead",
                        style={"margin-left": "190px", "margin-right": "190px"}
                    ),
                    width=12
                )
            ),
            dbc.Row(
                dbc.Col(
                    html.P(
                        [
                            "You can also stay updated with our progress and explore our open-source code on GitHub: ",
                            html.A("Weeks Bay Ultrasonic Depth Telemetry GitHub Repository", href="https://github.com/iadkins89/weeksBay_UltrasonicDepth_Telemetry"),
                        ],
                        className="lead",
                        style={"margin-left": "190px", "margin-right": "190px"}
                    ),
                    width=12
                )
            ),
        ],
        fluid=True
    )

    return layout

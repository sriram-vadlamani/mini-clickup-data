from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import requests
import json
import urllib
from datetime import datetime

pio.templates.default = "plotly_dark"

# Create the dash app
external_stylesheets = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            style={"textAlign": "center", "padding": "50px"},
            children=[
                html.H1("MiniClickup task log analysis"),
                dcc.Graph(id="time-series", figure={}),
            ],
        ),
    ]
)


@callback(
    Output(component_id="time-series", component_property="figure"),
    Input("url", "href"),
)
def get_data(pathname):
    parsed = urllib.parse.urlparse(pathname)
    parsed_dict = urllib.parse.parse_qs(parsed.query)
    user_name = parsed_dict["user"][0]
    print(user_name)
    url = "http://0.0.0.0:8080/export-logs?user=" + user_name
    task_logs = requests.request("GET", url).json()
    df = pd.DataFrame(task_logs)
    df["datetime"] = df["date"].apply(lambda x: datetime.fromtimestamp(x))
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["datetime"],
            y=df["time_spent"],
            mode="lines+markers",
            name="time_spent",
        )
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

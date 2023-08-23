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
                dcc.Graph(id="word-cloud", figure={}),
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
    url = "http://0.0.0.0:8080/export-logs?user=" + user_name
    print(url)
    task_logs = requests.get(url, verify=False).json()
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

    fig.update_layout(
        title="tasks logged over time",
        xaxis_title="Date",
        yaxis_title="Number of hours spent",
    )

    return fig


@callback(
    Output(component_id="word-cloud", component_property="figure"), Input("url", "href")
)
def get_tasks(pathname):
    parsed = urllib.parse.urlparse(pathname)
    parsed_dict = urllib.parse.parse_qs(parsed.query)
    user_name = parsed_dict["user"][0]
    url = "http://0.0.0.0:8080/export-tasks?user=" + user_name
    tasks = requests.get(url, verify=False).json()
    df = pd.DataFrame(tasks)

    fig = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=df["task_name"].nunique(),
            delta={"position": "top", "reference": 0},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )

    fig.update_layout(title="Number of total tasks")

    return fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=True)

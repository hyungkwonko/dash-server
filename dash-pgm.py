import dash
import dash_core_components as dcc
import dash_html_components as html

# import time
import plotly.graph_objs as go
import random
from collections import deque

import os
import pandas as pd


DATAPATH = os.path.join(os.getcwd(), "data")

DATASETS = {}
for k in range(10):
    DATASETS[f"TRIAL{k+1}"] = {
        "label": f"TRIAL{k+1}",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, f"trial{k+1}.csv"),
    }

# max_length = len(list(DATASETS['TRIAL1']['dataframe'].trial))
max_length = 11

for dataset in DATASETS:
    df = pd.read_csv(DATASETS[dataset]["datafile"], comment="#")
    df = random.sample(list(df["trial"]), k=max_length)
    DATASETS[dataset]["dataframe"] = sorted(df, reverse=True)

xs = [[] for i in range(10)]
ts = [[] for i in range(10)]
xs2 = []
ts2 = []

app = dash.Dash(
    name="PGM-project",
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"
    ],
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js"
    ],
)


data_dict = {
    "each trial (x) / metric (y)": ts,
    "trials (x) / best metric (y)": ts2,
}

app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "PGM Project: hyperparameter optimization", style={"float": "left",}
                ),
            ]
        ),
        dcc.Dropdown(
            id="graph-name",
            options=[{"label": s, "value": s} for s in data_dict.keys()],
            value=["each trial (x) / metric (y)", "trials (x) / best metric (y)"],
            multi=True,
        ),
        html.Div(children=html.Div(id="graphs"), className="row"),
        dcc.Interval(id="graph-update", interval=1000, n_intervals=0),
    ],
    className="container",
    style={"width": "98%", "margin-left": 10, "margin-right": 10, "max-width": 50000},
)


@app.callback(
    dash.dependencies.Output("graphs", "children"),
    [
        dash.dependencies.Input("graph-name", "value"),
        dash.dependencies.Input("graph-update", "n_intervals"),
    ],
)
def update_graph(data_names, n):
    NN = (n // max_length) + 1
    graphs = []
    datas = []

    if len(data_names) > 2:
        class_choice = "col s12 m6 l4"
    elif len(data_names) == 2:
        class_choice = "col s12 m6 l6"
    else:
        class_choice = "col s12"

    for j, data_name in enumerate(data_names):
        if j == 1:
            if NN == 1:
                continue
            if (n > 0) and (n % max_length == 0):
                ts2.append(min(DATASETS[f"TRIAL{NN-1}"]["dataframe"]))
                xs2.append(NN - 2)
            data2 = go.Scatter(x=list(xs2), y=list(ts2), mode="lines+markers",)
            graphs.append(
                html.Div(
                    dcc.Graph(
                        id=data_name,
                        animate=True,
                        figure={
                            "data": [data2],
                            "layout": go.Layout(
                                xaxis=dict(range=[0, 10], dtick=1.0),
                                yaxis=dict(
                                    range=[0, max(ts2, default=0.5)], dtick=0.02
                                ),
                                margin={"l": 50, "r": 1, "t": 45, "b": 1},
                                title=f"{data_name}",
                            ),
                        },
                    ),
                    className=class_choice,
                )
            )
        else:
            for i in range(NN):
                if (i + 1) == NN:  # append n-th element of trial-(i+1)
                    ts[i].append(
                        DATASETS[f"TRIAL{NN}"]["dataframe"][n - i * max_length]
                    )
                    xs[i].append(n - i * max_length)
                data = go.Scatter(
                    x=list(xs[i]),
                    y=list(ts[i]),
                    name=f"Trial{i+1}",
                    mode="lines+markers",
                )
                datas.append(data)

            graphs.append(
                html.Div(
                    dcc.Graph(
                        id=data_name,
                        animate=True,
                        figure={
                            "data": datas,
                            "layout": go.Layout(
                                xaxis=dict(range=[0, max_length], dtick=1.0),
                                yaxis=dict(range=[0, max(ts[0]) + 0.5], dtick=0.2),
                                margin={"l": 50, "r": 1, "t": 45, "b": 1},
                                title=f"{data_name}",
                            ),
                        },
                    ),
                    className=class_choice,
                )
            )

    return graphs


if __name__ == "__main__":
    app.run_server(debug=True)

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

DATASETS = {
    "TRIAL1": {
        "label": "TRIAL1",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, "trial1.csv"),
    },
    "TRIAL2": {
        "label": "TRIAL2",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, "trial2.csv"),
    },
    "TRIAL3": {
        "label": "TRIAL3",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, "trial3.csv"),
    },
    "TRIAL4": {
        "label": "TRIAL4",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, "trial4.csv"),
    },
    "TRIAL5": {
        "label": "TRIAL5",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, "trial5.csv"),
    },
    "TRIAL6": {
        "label": "TRIAL6",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, "trial6.csv"),
    },
    "TRIAL7": {
        "label": "TRIAL7",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, "trial7.csv"),
    },
    "TRIAL8": {
        "label": "TRIAL8",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, "trial8.csv"),
    },
    "TRIAL9": {
        "label": "TRIAL9",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, "trial9.csv"),
    },
    "TRIAL10": {
        "label": "TRIAL10",
        "dataframe": None,
        "datafile": os.path.join(DATAPATH, "trial10.csv"),
    },
}

# max_length = len(list(DATASETS['TRIAL1']['dataframe'].trial))
max_length = 10

for dataset in DATASETS:
    df = pd.read_csv(DATASETS[dataset]["datafile"], comment="#")
    df = random.sample(list(df["trial"]), k=max_length)
    DATASETS[dataset]["dataframe"] = sorted(df, reverse=True)

xs = [[] for i in range(10)]
ts = [[] for i in range(10)]

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id="live-graph", animate=True),
        dcc.Interval(id="graph-update", interval=1 * 1000, n_intervals=0,),
    ]
)


@app.callback(
    dash.dependencies.Output("live-graph", "figure"),
    [dash.dependencies.Input("graph-update", "n_intervals"),],
)
def update_graph(n):
    NN = (n // max_length) + 1
    cur_data = DATASETS[f"TRIAL{NN}"]["dataframe"]

    # t1.append(DATASETS['TRIAL1']['dataframe'][n]) # append n-th element of trial-1
    # t2.append(DATASETS['TRIAL10']['dataframe'][n])

    datas = []
    for i in range(NN):
        if (i + 1) == NN:  # append n-th element of trial-(i+1)
            ts[i].append(cur_data[n - i * max_length])
            xs[i].append(n - i * max_length)
        data = go.Scatter(
            x=list(xs[i]), y=list(ts[i]), name=f"Trial{i+1}", mode="lines+markers"
        )
        datas.append(data)

    return {
        "data": datas,
        "layout": go.Layout(
            xaxis=dict(range=[0, max_length]), yaxis=dict(range=[0, max(ts[0])]),
        ),
    }


if __name__ == "__main__":
    app.run_server(debug=True)

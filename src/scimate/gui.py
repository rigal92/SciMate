import numpy as np
import sys
import pandas as pd 
import scimate.mappingtools as mapt
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.io as pio
from dash import Dash, dcc, html, Input, Output, callback

pio.templates.default = "plotly_white"

# --- Dash app ---
def make_app():
    app = Dash(__name__)

    app.layout = html.Div([
        html.H2("Interactive Spectra Map"),

        html.Div([
            dcc.Graph(id="map", style={"display": "inline-block"}),
            dcc.Graph(id="spectrum", style={"display": "inline-block"})
        ], style={"display": "flex"})
        ]
    )

    return app

# initial map
@callback(
    Output("map", "figure"),
    Input("map", "id")
)
def draw_map(_):
    fig = go.Figure(data=go.Heatmap(
        z=data["z"],
        colorscale="Viridis"
    ))
    fig.update_layout(title="Spectra Intensity Map",    
        xaxis=dict(title="X", scaleanchor="y"), 
        yaxis=dict(title="Y", scaleratio=1)
            )
    return fig

# click event -> spectrum
@callback(
    Output("spectrum", "figure"),
    Input("map", "clickData")
)
def show_spectrum(clickData):
    if clickData is None:
        return go.Figure()

    # get clicked pixel index
    i = clickData["points"][0]["x"]
    j = clickData["points"][0]["y"]
    idx = j * ny + i  # flatten index

    # col = df.columns[idx+1]  # +1 to skip 'x'
    y = spectra.iloc[:,idx]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_spec, y=y, mode="lines"))
    fig.update_layout(title=f"Spectrum at pixel ({i},{j})", xaxis_title="x", yaxis_title="Intensity")
    return fig

def initialize_data(filename, nx, ny, file_format="jasco"):
    df = mapt.read_map(filename, file_format)
    spectra = df.iloc[:,1:]
    x = spectra.columns.get_level_values(0).astype(float)
    y = spectra.columns.get_level_values(1).astype(float)
    xrel = x-x.min()
    yrel = y-y.min()
    z = spectra.sum().values.reshape(ny,nx)
    z = z/z.max()
    return dict(x=x, y=y, xrel=xrel, yrel=yrel, z=z, df=df)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("")
    parser.add_argument("filename", help="file containg the spectra")
    parser.add_argument("nx", help="number of points in x")
    parser.add_argument("ny", help="number of points in y")
    parser.add_argument("--mode", default="spectra", help="Choose what to plot alongside with the intensity map. 'spectra' is allowed.")
    args = parser.parse_args()

    filename = args.filename
    nx = int(args.nx)
    ny = int(args.ny)
    data = initialize_data(filename, nx, ny)
    x_spec = data["df"].iloc[:,0]
    spectra = data["df"].iloc[:,1:]
    app = make_app()
    app.run(debug=True)
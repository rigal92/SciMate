import numpy as np
import sys
import pandas as pd 
import scimate.mappingtools as mapt
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output, callback

# --- Example DataFrame (replace with your real one) ---
x = np.linspace(400, 800, 200)  # e.g. wavelengths
spectra = {f"pixel_{i}": np.sin(0.02 * x + i) + np.random.rand(len(x))*0.1 for i in range(100)}
df = pd.DataFrame({"x": x, **spectra})

# reshape spectra into a square map (here 10x10)
map_size = int(np.sqrt(len(df.columns)-1))
map_data = np.array([df[col].sum() for col in df.columns[1:]]).reshape(map_size, map_size)

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
    idx = j * map_size + i  # flatten index

    # col = df.columns[idx+1]  # +1 to skip 'x'
    y = spectra.iloc[:,idx]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_spec, y=y, mode="lines"))
    fig.update_layout(title=f"Spectrum at pixel ({i},{j})", xaxis_title="x", yaxis_title="Intensity")
    return fig

def initialize_data(filename, nx, ny):
    df = pd.read_table(filename, header = [13,14])
    spectra = df.iloc[:,1:]
    x = spectra.columns.get_level_values(0).astype(float)
    y = spectra.columns.get_level_values(1).astype(float)
    xrel = x-x.min()
    yrel = y-y.min()
    z = spectra.sum().values.reshape(nx,ny)
    z = z/z.max()
    return dict(x=x, y=y, xrel=xrel, yrel=yrel, z=z, df=df)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python app.py <spectra_file.csv> <nx> <ny>")
        sys.exit(1)

    filename = sys.argv[1]
    nx = int(sys.argv[2])
    ny = int(sys.argv[3])
    data = initialize_data(filename, nx, ny)
    x_spec = data["df"].iloc[:,0]
    spectra = data["df"].iloc[:,1:]
    app = make_app()
    app.run(debug=True)
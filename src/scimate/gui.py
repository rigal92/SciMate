import numpy as np
import pandas as pd 
import scimate.mappingtools as mapt
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

# --- Example DataFrame (replace with your real one) ---
x = np.linspace(400, 800, 200)  # e.g. wavelengths
spectra = {f"pixel_{i}": np.sin(0.02 * x + i) + np.random.rand(len(x))*0.1 for i in range(100)}
df = pd.DataFrame({"x": x, **spectra})

# reshape spectra into a square map (here 10x10)
map_size = int(np.sqrt(len(df.columns)-1))
map_data = np.array([df[col].sum() for col in df.columns[1:]]).reshape(map_size, map_size)

# --- Dash app ---
app = Dash(__name__)

app.layout =html.Div([
        dcc.Graph(id="map", style={"display": "inline-block"}),
        dcc.Graph(id="spectrum", style={"display": "inline-block"})
    ], style={"display": "flex"})

# initial map
@app.callback(
    Output("map", "figure"),
    Input("map", "id")
)
def draw_map(_):
    fig = go.Figure(data=go.Heatmap(
        z=map_data,
        colorscale="Viridis"
    ))
    fig.update_layout(title="Spectra Intensity Map",    
        xaxis=dict(title="X",range=[-0.5, map_size - 0.5],scaleanchor="y"), 
        yaxis=dict(title="Y",range=[-0.5, map_size - 0.5],scaleratio=1)
            )
    return fig

# click event -> spectrum
@app.callback(
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

    col = df.columns[idx+1]  # +1 to skip 'x'
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["x"], y=df[col], mode="lines", name=col))
    fig.update_layout(title=f"Spectrum at pixel ({i},{j})", xaxis_title="x", yaxis_title="Intensity")
    return fig

def main():
    app.run(debug=True)
import os, textwrap, zipfile, pathlib, json, re, datetime
base = "/mnt/data/interactive-3d-surface-app"
os.makedirs(base, exist_ok=True)

app_py = r'''
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Interactive 3D Surface", layout="wide")

st.title("Interactive 3D Surface")
st.caption("y = sin(a·x) · cos(b·z)")

with st.sidebar:
    st.header("Controls")
    a = st.slider("a (x frequency)", 0.1, 10.0, 3.1, 0.1)
    b = st.slider("b (z frequency)", 0.1, 10.0, 0.8, 0.1)
    domain = st.slider("Domain (±)", 1, 20, 10, 1)
    resolution = st.slider("Resolution", 30, 300, 120, 10)
    st.markdown("---")
    st.write("Tip: higher resolution = smoother surface, but slower.")

# Grid
x = np.linspace(-domain, domain, resolution)
z = np.linspace(-domain, domain, resolution)
X, Z = np.meshgrid(x, z)
Y = np.sin(a * X) * np.cos(b * Z)

# Plotly 3D surface
surface = go.Surface(x=X, y=Z, z=Y)  # y-axis used for z values to match labels below
fig = go.Figure(data=[surface])

fig.update_layout(
    margin=dict(l=0, r=0, t=40, b=0),
    scene=dict(
        xaxis_title="x",
        yaxis_title="z",
        zaxis_title="y",
    ),
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Show data / equation details"):
    st.latex(r"y = \sin(a x)\cdot \cos(b z)")
    st.write("Current parameters:", {"a": a, "b": b, "domain": domain, "resolution": resolution})
'''

requirements = """streamlit>=1.31
plotly>=5.18
numpy>=1.24
"""

readme = """# Interactive 3D Surface (Streamlit)

An interactive web app that visualizes:

**y = sin(a·x) · cos(b·z)**

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py



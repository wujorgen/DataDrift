import pandas as pd
import plotly.graph_objects as go
from BLUESKY.scrapers import scraper

data = scraper.spider_results()

columns = ["make", "model", "model_year", "trim", "mileage", "price"]

df = pd.DataFrame(data, columns=columns)
df["mileage"] = (
    df["mileage"].str.replace(",", "").str.extract("(\d+)", expand=False).astype(float)
)
df["model_year"] = df["model_year"].astype(float)

print(df)

mustangs = df[
    (df["make"] == "ford")
    & (df["model"] == "mustang")
    & (df["trim"].str.contains("gt"))
]
supras = df[
    (df["make"] == "toyota")
    & (df["model"] == "supra")
    & (df["trim"].str.contains("3.0"))
]

print(mustangs)

print(supras)

fig1 = go.Figure(
    data=go.Scatter3d(
        x=mustangs["model_year"],
        y=mustangs["mileage"],
        z=mustangs["price"],
        mode="markers",
        marker=dict(size=5, color=mustangs["price"], colorscale="Viridis", opacity=0.8),
    )
)

fig1.update_layout(
    scene=dict(
        xaxis=dict(title="MODEL YEAR"),
        yaxis=dict(title="MILEAGE"),
        zaxis=dict(title="PRICE"),
    ),
    title="DEPRECIATION SURFACE FOR THE FORD MUSTANG GT",
)

fig1.show()

fig2 = go.Figure(
    data=go.Scatter3d(
        x=supras["model_year"],
        y=supras["mileage"],
        z=supras["price"],
        mode="markers",
        marker=dict(size=5, color=supras["price"], colorscale="Viridis", opacity=0.8),
    )
)

fig2.update_layout(
    scene=dict(
        xaxis=dict(title="MODEL YEAR"),
        yaxis=dict(title="MILEAGE"),
        zaxis=dict(title="PRICE"),
    ),
    title="DEPRECIATION SURFACE FOR THE MK5 TOYOTA SUPRA 3.0",
)

fig2.show()

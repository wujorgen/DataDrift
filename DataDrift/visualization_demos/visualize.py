"""DEMO OF VISUALIZATION"""

import pandas as pd
import plotly.graph_objects as go

from DataDrift.scrapers import soup_scraper as scraper

start_urls = [
    "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true",
    "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=toyota&models=toyota-supra&clean_title=true&no_accidents=true&personal_use=true",
]

data = scraper.scrape_data_payload(urls=start_urls)

columns = ["make", "model", "model_year", "trim", "mileage", "price", "listing_id"]

df = pd.DataFrame(data, columns=columns)
df["mileage"] = (
    df["mileage"].str.replace(",", "").str.extract("(\d+)", expand=False).astype(float)
)
df["model_year"] = df["model_year"].astype(float)

df["listing_id"] = '<a href="cars.com/vehicledetail/' + df["listing_id"] + '">name</a>'

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

print("<><><>")
print(mustangs)
print("<><><>")
print(supras)
print("<><><>")

fig1 = go.Figure(
    data=go.Scatter3d(
        x=mustangs["model_year"],
        y=mustangs["mileage"],
        z=mustangs["price"],
        mode="markers",
        marker=dict(size=5, color=mustangs["price"], colorscale="Viridis", opacity=0.8),
        customdata=mustangs["listing_id"],
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
        customdata=supras["listing_id"],
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

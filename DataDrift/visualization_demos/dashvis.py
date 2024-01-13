import webbrowser

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # noqa F401
from dash import dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from DataDrift.scrapers import bs4_scraper as scraper

# GET DATA #
start_urls = [
    "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=ford&models=ford-mustang&trims=ford-mustang-gt&clean_title=true&no_accidents=true&personal_use=true",  # noqa E501
    "https://www.cars.com/shopping/results/?stock_type=all&zip=15024&maximum_distance=500&makes=toyota&models=toyota-supra&clean_title=true&no_accidents=true&personal_use=true",  # noqa E501
]

data = scraper.scrape_data_payload(urls=start_urls)

# PROCESS DATA #
columns = ["make", "model", "model_year", "trim", "mileage", "price", "listing_id"]

df = pd.DataFrame(data, columns=columns)
df["mileage"] = (
    df["mileage"].str.replace(",", "").str.extract(r"(\d+)", expand=False).astype(float)
)
df["model_year"] = df["model_year"].astype(float)

df["listing_id"] = "cars.com/vehicledetail/" + df["listing_id"]

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

# DASH APP #
app = dash.Dash(__name__)
app.title = "Vehicle Depreciation Surface"
df = pd.DataFrame(
    dict(
        MODEL_YEAR=mustangs["model_year"],
        MILEAGE=mustangs["mileage"],
        PRICE=mustangs["price"],
        urls=mustangs["listing_id"],
    )
)
app.layout = html.Div(
    children=[
        dcc.Graph(
            id="3D-SURFACE",
            figure=px.scatter_3d(
                title="Ford Mustang Depreciation Surface",
                data_frame=df,
                x="MODEL_YEAR",
                y="MILEAGE",
                z="PRICE",
                custom_data=("urls",),
            ),
            style={
                "width": "95vw",
                "height": "60vh",
            },
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            id="YEARxPRICE",
                            figure=px.scatter(
                                title="Ford Mustang Depreciation by Year",
                                data_frame=df,
                                x="MODEL_YEAR",
                                y="PRICE",
                            ),
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "3vw",
                    },
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            id="MILEAGExPRICE",
                            figure=px.scatter(
                                title="Ford Mustang Depreciation by Mileage",
                                data_frame=df,
                                x="MILEAGE",
                                y="PRICE",
                            ),
                        ),
                    ],
                    style={
                        "display": "inline-block",
                        "vertical-align": "top",
                        "margin-left": "3vw",
                        "margin-top": "3vw",
                    },
                ),
            ]
        ),
    ]
)


@app.callback(Output("3D-SURFACE", "figure"), [Input("3D-SURFACE", "clickData")])
def open_url(clickData):
    print(clickData)
    if clickData is not None:
        url = clickData["points"][0]["customdata"][0]
        webbrowser.open_new_tab(url)
    else:
        raise PreventUpdate


app.run_server()

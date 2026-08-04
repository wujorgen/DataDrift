import streamlit as st
import numpy as np
from scipy.interpolate import griddata
from DataDrift.analytics.curve_fitting import fit_exponential_curve
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def chart_price_v_miles(df:pd.DataFrame) -> go.Figure:
    # Construct an empty figure with an instructional message
    fig = go.Figure()
    fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[
            {
                "text": "No Trims Selected",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 18, "color": "gray"},
            }
        ],
        height=500,
    )
    #available_trims = sorted(df["trim"].unique().tolist())
    available_trims = df["trim"].unique()
    selected_trims = st.multiselect(
        "Filter / Fit Specific Trims:",
        options=available_trims,
        default=available_trims,
    )
    # Filter dataframe to selected trims
    filtered_df = df[df["trim"].isin(selected_trims)].dropna()
    if filtered_df.empty:
        st.info("Please select at least one trim to view scatter data.")
    else:
        fig = px.scatter(
            filtered_df,
            x="miles",
            y="price",
            color="trim",
            symbol="year",
            title=f"Price vs. Mileage for Selected Trims",
            labels={
                "miles": "Mileage (miles)",
                "price": "Price ($)",
                "trim": "Trim Level",
            },
            hover_data=["year", "city"],
            height=550,
        )
        # Fit curve too all selected trims
        fit_result = fit_exponential_curve(
            filtered_df, x_col="miles", y_col="price"
        )
        if fit_result is not None:
            x_smooth, y_smooth, params = fit_result
            a, b, c = params
            fig.add_trace(
                go.Scatter(
                    x=x_smooth,
                    y=y_smooth,
                    mode="lines",
                    name=f"Fit",
                    line=dict(dash="dash", width=2.5),
                    hovertemplate=f"<b>Trend</b><br>Miles: %{{x:,.0f}}<br>Est Price: $%{{y:,.2f}}<extra></extra>",
                )
            )
            st.caption(
                f"**Fitted Model Equation:** $\\text{{Price}} = {a:,.2f} \\cdot e^{{-{b:.6f} \\cdot \\text{{Miles}}}} + {c:,.2f}$"
            )
    return fig


def chart_price_distribution(df:pd.DataFrame) -> go.Figure:
    fig = px.box(
        df,
        x="year",
        y="price",
        color="trim",
        title=f"Price Distribution by Model Year",
        labels={"year": "Model Year", "price": "Price ($)"},
        height=500,
    )
    return fig


def chart_price_trend(df:pd.DataFrame) -> go.Figure:
    avg_df = df.groupby(["year", "trim"])["price"].mean().reset_index()
    fig = px.line(
        avg_df,
        x="year",
        y="price",
        color="trim",
        markers=True,
        title=f"Average Market Price Trend Across Model Years",
        labels={"year": "Model Year", "price": "Average Price ($)"},
        height=500,
    )
    return fig


def chart_mileage_trend(df:pd.DataFrame) -> go.Figure:
    avg_df = df.groupby(["year", "trim"])["miles"].mean().reset_index()
    fig = px.line(
        avg_df,
        x="year",
        y="miles",
        color="trim",
        markers=True,
        title=f"Average Mileage Trend Across Model Years",
        labels={"year": "Model Year", "miles": "Average Mileage (mi)"},
        height=500,
    )
    return fig


def chart_3d_surface(df:pd.DataFrame) -> go.Figure:
    """
    Transforms raw Marketcheck DataFrame into a 3D Surface plot
    (X: Mileage, Y: Model Year, Z: Price).
    """
    # Clean and isolate numeric columns
    clean_df = df.dropna(subset=["miles", "year", "price"]).copy()
    
    if len(clean_df) < 4:
        # Surface interpolation requires at least 4 distinct spatial points
        return None

    # Extract coordinates
    x_data = clean_df["miles"].values
    y_data = clean_df["year"].values
    z_data = clean_df["price"].values

    # 1. Create a uniform 2D grid covering the mileage and year space
    x_grid = np.linspace(x_data.min(), x_data.max(), 30)
    y_grid = np.linspace(y_data.min(), y_data.max(), 30)
    X, Y = np.meshgrid(x_grid, y_grid)

    # 2. Interpolate prices (Z) across the 2D grid
    Z = griddata(
        points=(x_data, y_data),
        values=z_data,
        xi=(X, Y),
        method="linear"  # 'linear' or 'cubic' for smooth interpolation
    )

    # 3. Build Plotly 3D Surface
    fig = go.Figure()

    # Add the continuous interpolated surface
    fig.add_trace(
        go.Surface(
            x=x_grid,
            y=y_grid,
            z=Z,
            colorscale="Viridis",
            colorbar=dict(title="Price ($)"),
            name="Market Surface"
        )
    )

    # Add actual car listings as 3D scatter points on top of the surface
    fig.add_trace(
        go.Scatter3d(
            x=x_data,
            y=y_data,
            z=z_data,
            mode="markers",
            marker=dict(size=4, color="red", opacity=0.8),
            name="Actual Listings"
        )
    )

    # Layout styling for Streamlit
    fig.update_layout(
        title="Car Depreciation Surface (Price vs. Mileage & Year)",
        scene=dict(
            xaxis_title="Mileage",
            yaxis_title="Model Year",
            zaxis_title="Price ($)"
        ),
        autosize=True,
        margin=dict(l=20, r=20, b=20, t=50)
    )

    return fig


CHART_TYPES = {
    "Price vs. Miles (by Trim)": chart_price_v_miles,
    "Price Distribution (by Year)": chart_price_distribution,
    "Price Trend (Yearly Average)": chart_price_trend,
    "Mileage Trend (Yearly Average)": chart_mileage_trend,
    "3D Price & Mileage Surface": chart_3d_surface,
}
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.optimize import curve_fit
import random

def exponential_decay(x, a, b, c):
    """ Exponential model: y = a * exp(-b * x) + c """
    return a * np.exp(-b * x) + c

def fit_exponential_curve(df, x_col="miles", y_col="price"):
    """
    Fits exponential decay parameters (a, b, c) and generates smooth 
    curve points for plotting.
    """
    if len(df) < 3:
        return None  # Need at least 3 points to fit 3 parameters

    x_data = df[x_col].values
    y_data = df[y_col].values

    # Initial guesses: A ~ price range, b ~ small decay factor, C ~ min price
    initial_guess = (y_data.max() - y_data.min(), 0.00003, y_data.min())

    try:
        # Fit curve using non-linear least squares
        popt, _ = curve_fit(
            exponential_decay, 
            x_data, 
            y_data, 
            p0=initial_guess, 
            bounds=(0, [np.inf, 1.0, np.inf]),
            maxfev=5000
        )
        
        # Generate smooth X values for drawing the line
        x_smooth = np.linspace(x_data.min(), x_data.max(), 100)
        y_smooth = exponential_decay(x_smooth, *popt)

        return x_smooth, y_smooth, popt
    except Exception as e:
        # Returns None if optimization fails to converge
        return None



def fetch_marketcheck_mock_data(make: str, model: str, year_start: int, year_end: int) -> pd.DataFrame:
    """
    Mock function to simulate fetching data across dynamic user query parameters.
    Replace this with your actual Marketcheck API request via `requests`.
    """
    records = []
    
    # Generic mock generator adapting to whatever input the user types
    trims = ["Base", "Sport", "Touring", "Performance", "Limited"]
    
    for i in range(50):
        y = random.randint(year_start, year_end)
        trim = random.choice(trims)
        age = max(0, current_year - y)
        
        # Estimate realistic mileage & depreciated pricing relative to vehicle age
        miles = max(500, int(age * random.uniform(7000, 13000) + random.randint(-1000, 3000)))
        base = 35000
        depreciation = max(0.20, 1.0 - (age * 0.07))
        price = int(base * depreciation + random.randint(-3000, 5000))

        records.append({
            "id": f"mkck_{1000 + i}",
            "year": y,
            "make": make.title(),
            "model": model.title(),
            "trim": trim,
            "price": max(price, 3000),
            "miles": miles,
            "city": random.choice(["Austin, TX", "Los Angeles, CA", "Miami, FL", "Chicago, IL"])
        })

    return pd.DataFrame(records)


# 1. Page Configuration
st.set_page_config(page_title="Marketcheck Car Dashboard", layout="wide")
st.title("🚗 Marketcheck Car Listings Dashboard")

# Initialize session state for holding fetched data across re-renders
if "car_df" not in st.session_state:
    st.session_state.car_df = None

# 2. Sidebar Search Controls
st.sidebar.header("Search Filters")

# Secure API Key input
api_key = st.sidebar.text_input("API Key", type="password", help="Enter your Marketcheck API key")

# Freeform text inputs with no default values
make = st.sidebar.text_input("Make", value="", placeholder="e.g. Ford")
model = st.sidebar.text_input("Model", value="", placeholder="e.g. Mustang")

# Dynamic upper bound: Current Year + 1 (handles upcoming OEM model years)
current_year = datetime.now().year
min_model_year = st.sidebar.number_input(
    "Min Year", 
    min_value=1900, 
    max_value=current_year + 1, 
    value=1900, 
    step=1
)
max_model_year = st.sidebar.number_input(
    "Max Year", 
    min_value=1900, 
    max_value=current_year + 1, 
    value=current_year + 1, 
    step=1
)

# 3. Trigger API Call
if st.sidebar.button("Fetch Car Data", type="primary"):
    if not api_key:
        st.warning("Please enter your API Key before searching.")
    elif not make or not model:
        st.warning("Please specify both a Make and Model.")
    else:
        with st.spinner(f"Querying Marketcheck API for {make} {model}..."):
            # Execute mock fetch (or call your real requests helper here)
            st.session_state.car_df = fetch_marketcheck_mock_data(
                make, model, min_model_year, max_model_year
            )
            st.session_state.query_label = f"{make.title()} {model.title()} ({min_model_year}-{max_model_year})"

# 4. Main Panel - Render Data & Plotly Visualization
if st.session_state.car_df is not None:
    df = st.session_state.car_df
    label = st.session_state.get("query_label", "Vehicles")

    if df.empty:
        st.info("No listings found matching your parameters.")
    else:
        # Key Summary Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Listings", len(df))
        m2.metric("Average Price", f"${df['price'].mean():,.2f}")
        m3.metric("Average Mileage", f"{df['miles'].mean():,.0f} mi")
        m4.metric("Lowest Price", f"${df['price'].min():,.2f}")

        st.divider()

        # Plot Controls Header
        header_col, control_col = st.columns([2.5, 1.5])

        with header_col:
            st.subheader(f"Analytics: {label}")

        with control_col:
            chart_type = st.selectbox(
                "Select Visualization View",
                ["Price vs. Miles (by Trim)", "Price Distribution (by Year)", "Price Trend (Yearly Average)"],
                key="chart_picker"
            )

        # 5. Plotly Figure Rendering using cached session state data
        if chart_type == "Price vs. Miles (by Trim)":
            # Construct an empty figure with an instructional message
            fig = go.Figure()
            fig.update_layout(
                xaxis={"visible": False},
                yaxis={"visible": False},
                annotations=[{
                    "text": "No Trims Selected",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 18, "color": "gray"}
                }],
                height=500
            )
            available_trims = sorted(df["trim"].unique().tolist())
            selected_trims = st.multiselect(
                "Filter / Fit Specific Trims:",
                options=available_trims,
                default=available_trims,
            )
            # Filter dataframe to selected trims
            filtered_df = df[df["trim"].isin(selected_trims)]
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
                fit_result = fit_exponential_curve(filtered_df, x_col="miles", y_col="price")
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
        elif chart_type == "Price Distribution (by Year)":
            fig = px.box(
                df,
                x="year",
                y="price",
                color="trim",
                title=f"Price Distribution by Model Year",
                labels={"year": "Model Year", "price": "Price ($)"},
                height=500
            )
        else:  # Price Trend
            avg_df = df.groupby(["year", "trim"])["price"].mean().reset_index()
            fig = px.line(
                avg_df,
                x="year",
                y="price",
                color="trim",
                markers=True,
                title=f"Average Market Price Trend Across Model Years",
                labels={"year": "Model Year", "price": "Average Price ($)"},
                height=500
            )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Explore Raw Marketcheck Dataset"):
            st.dataframe(df, use_container_width=True)
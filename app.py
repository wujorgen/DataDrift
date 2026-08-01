from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Replace with your actual package import path
from DataDrift.clients.marketcheck_client import MarketcheckClient, SampleClient
from DataDrift.analytics.curve_fitting import fit_exponential_curve

# 1. Page Configuration
st.set_page_config(page_title="Marketcheck Car Dashboard", layout="wide")
st.title("🚗 Marketcheck Car Listings Dashboard")

# Initialize session state for holding fetched data across re-renders
if "car_df" not in st.session_state:
    st.session_state.car_df = None

# 2. Sidebar Search Controls
st.sidebar.header("Search Filters")

# Secure API Key input
api_key = st.sidebar.text_input(
    "API Key", type="password", help="Enter your Marketcheck API key"
)

# Optional toggle for developer/offline testing
use_sample_data = st.sidebar.checkbox("Use Sample Local Data", value=False)


@st.cache_resource
def get_marketcheck_client(
    api_key: str, use_sample: bool
) -> MarketcheckClient | SampleClient:
    """Instantiates and caches the API client instance."""
    if use_sample:
        return SampleClient(api_key=api_key)
    return MarketcheckClient(api_key=api_key)


@st.cache_data(ttl=3600)  # Caches results for 1 hour (3600 seconds)
def fetch_listings(
    _client: MarketcheckClient | SampleClient,
    make: str,
    model: str,
    year_min: int,
    year_max: int,
) -> pd.DataFrame:
    """
    Fetches listings from Marketcheck API or Sample client and cleans into a DataFrame.
    Prefixing _client with an underscore prevents Streamlit from un-hashable object errors.
    """
    raw_listings = _client.fetch_vehicle_data(
        make=make,
        model=model,
        year_min=year_min,
        year_max=year_max,
    )

    if not raw_listings:
        return pd.DataFrame()

    # Parse nested Marketcheck JSON payload into a clean flat DataFrame
    records = []
    for item in raw_listings:
        build = item.get("build", {})
        dealer = item.get("dealer", {})
        records.append(
            {
                "id": item.get("id"),
                "year": build.get("year"),
                "make": build.get("make"),
                "model": build.get("model"),
                "trim": build.get("trim"),
                "price": item.get("price"),
                "miles": item.get("miles"),
                "city": dealer.get("city"),
                "zip": dealer.get("zip"),
                "url": item.get("vdp_url"),
            }
        )

    return pd.DataFrame(records)


# Search Form Inputs
make = st.sidebar.text_input("Make", value="", placeholder="e.g. Ford")
model = st.sidebar.text_input("Model", value="", placeholder="e.g. Mustang")

current_year = datetime.now().year
min_model_year = st.sidebar.number_input(
    "Min Year", min_value=1900, max_value=current_year + 1, value=2015, step=1
)
max_model_year = st.sidebar.number_input(
    "Max Year",
    min_value=1900,
    max_value=current_year + 1,
    value=current_year + 1,
    step=1,
)

# Fetch Trigger Button
if st.sidebar.button("Search Inventory", type="primary"):
    if not make or not model:
        st.warning("Please enter both a Make and Model.")
    elif not api_key and not use_sample_data:
        st.error("Please provide a Marketcheck API key.")
    else:
        # Get cached client
        client = get_marketcheck_client(api_key, use_sample_data)

        with st.spinner(f"Fetching {make} {model} listings..."):
            try:
                df = fetch_listings(client, make, model, min_model_year, max_model_year)
                st.session_state.car_df = df

                if df.empty:
                    st.info("No listings found matching your search criteria.")
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")


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
                [
                    "Price vs. Miles (by Trim)",
                    "Price Distribution (by Year)",
                    "Price Trend (Yearly Average)",
                ],
                key="chart_picker",
            )

        # 5. Plotly Figure Rendering using cached session state data
        if chart_type == "Price vs. Miles (by Trim)":
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
        elif chart_type == "Price Distribution (by Year)":
            fig = px.box(
                df,
                x="year",
                y="price",
                color="trim",
                title=f"Price Distribution by Model Year",
                labels={"year": "Model Year", "price": "Price ($)"},
                height=500,
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
                height=500,
            )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Explore Raw Marketcheck Dataset"):
            st.dataframe(df, use_container_width=True)

from datetime import datetime

import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Replace with your actual package import path
from DataDrift.clients import get_marketcheck_client, fetch_listings, MarketcheckClient, SampleClient
from DataDrift.analytics.curve_fitting import fit_exponential_curve
from DataDrift.charts import CHART_TYPES

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
                CHART_TYPES.keys(),
                key="chart_picker",
            )

        # 5. Plotly Figure Rendering using cached session state data
        fig = CHART_TYPES[chart_type](df)

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("Explore Raw Marketcheck Dataset"):
            st.dataframe(df, use_container_width=True)

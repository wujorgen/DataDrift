from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
import random

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
            fig = px.scatter(
                df,
                x="miles",
                y="price",
                color="trim",
                symbol="year",
                title=f"Price vs. Mileage for {label}",
                labels={"miles": "Mileage (miles)", "price": "Price ($)", "trim": "Trim Level"},
                hover_data=["year", "city"],
                height=500
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
import streamlit as st

# Set page title and layout
st.set_page_config(page_title="Marketcheck Vehicle Search", layout="wide")

st.title("🚗 Marketcheck Car Tracker")
st.write("Welcome! Use the sidebar to configure your search parameters.")

# Sidebar controls
st.sidebar.header("Search Filters")
make = st.sidebar.text_input("Make", value="BMW")
model = st.sidebar.text_input("Model", value="M3")
year_range = st.sidebar.slider("Year Range", 1990, 2026, (2021, 2026))

# Main content button
if st.button("Search Vehicles"):
    st.success(f"Searching for {make} {model} between {year_range[0]} and {year_range[1]}...")
    
    # Placeholder for your API logic
    st.json({
        "status": "Success",
        "query": {
            "make": make,
            "model": model,
            "years": f"{year_range[0]}-{year_range[1]}"
        }
    })
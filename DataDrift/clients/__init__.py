from .marketcheck_client import MarketcheckClient, SampleClient
import pandas as pd
import streamlit as st


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

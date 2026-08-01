import json
import os
import requests


class MarketcheckClient:
    """
    API Client wrapper for Marketcheck services.
    Uses requests.Session() to maintain TCP connection pooling across queries.
    """

    BASE_URL = "https://api.marketcheck.com/v2/search/car/active"

    def __init__(self, api_key: str):
        self.api_key = api_key
        # Actually create the session for connection reuse!
        self.session = requests.Session()

    def fetch_vehicle_data(
        self,
        make: str,
        model: str,
        year_min: int,
        year_max: int,
        trim: str = "",
        car_type: str = "used",
        number: int = 50,
    ) -> list[dict]:
        """Fetches active car listings from Marketcheck API."""
        all_listings = []
        page_size = 50  # Free Tier limit per request
        year_range = f"{year_min}-{year_max}"

        for start in range(0, number, page_size):
            params = {
                "api_key": self.api_key,
                "rows": min(page_size, number - start),
                "start": start,
                "stats": "price,miles,dom_active",
                "make": make.lower(),
                "model": model.lower(),
                "year_range": year_range,
                "car_type": car_type,
            }
            if trim != "":
                params["trim"] = trim

            # Use persistent self.session instead of generic requests
            resp = self.session.get(self.BASE_URL, params=params, timeout=30)

            if resp.status_code != 200:
                raise RuntimeError(
                    f"Marketcheck API error {resp.status_code}: {resp.text[:500]}"
                )

            data = resp.json()
            listings = data.get("listings", [])
            all_listings.extend(listings)

            # Stop early if end of pagination is reached
            if not listings or len(listings) < page_size:
                break

        return all_listings


class SampleClient:
    """Mock client for local testing using offline JSON files."""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key

    def fetch_vehicle_data(
        self,
        make: str,
        model: str,
        year_min: int = 1900,
        year_max: int = 2026,
        trim: str = "",
        car_type: str = "used",
        number: int = 50,
    ) -> list[dict]:
        """Signature matches MarketcheckClient"""
        basepath = os.path.dirname(__file__)
        fname = os.path.join(
            basepath, "sample-data", f"{make.lower()}_{model.replace(" ", "%20").lower()}.json"
        )
        
        if not os.path.exists(fname):
            return []

        with open(fname, "r") as f:
            listings = json.load(f)
            
        return listings

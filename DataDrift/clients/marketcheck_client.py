import requests
import os
import json

class MarketcheckClient:
    """
    API Client wrapper for Marketcheck services.
    Uses requests.Session() to maintain connection pooling across requests.
    """
    BASE_URL = "https://api.marketcheck.com/v2/search/car/active"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_vehicle_data(self, make, model, year_range, trim: str = "", car_type: str = "used", number: int = 50):
        """Fetches vehicle data from MarketCheck, including active listings.

        :param str make:
        :param str model:
        :param str year_range:
        :param str trim:
        :param str car_type:
        :param int number: 
        """
        all_listings = []
        page_size = 50  # Match the Free Tier limit per API request
        
        for start in range(0, number, page_size):
            params = {
                "api_key": self.api_key,
                "rows": min(page_size, number - start),
                "start": start,
                "stats": "price,miles,dom_active",
                "make": make,
                "model": model,
                "year_range": year_range,
                "car_type": car_type,
            }
            if trim != "":
                params["trim"] = trim
            resp = requests.get(self.BASE_URL, params=params, timeout=30)
            
            if resp.status_code != 200:
                raise RuntimeError(f"Marketcheck API error {resp.status_code}: {resp.text[:500]}")
                
            data = resp.json()
            listings = data.get("listings", [])
            all_listings.extend(listings)
            
            # Stop early if no more listings are returned
            if not listings or len(listings) < page_size:
                break
                
        return all_listings


class SampleClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_vehicle_data(self, make, model):
        basepath = os.path.dirname(__file__)
        fname = os.path.join(basepath, "sample-data", f"{make.lower()}_{model.lower()}.json")
        with open(fname, "r") as f:
            listings = json.load(f)
        return listings

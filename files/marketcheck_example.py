#%%
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
import sys

API_KEY = os.environ.get("MARKETCHECK_API_KEY")

BASE_URL = "https://api.marketcheck.com/v2/search/car/active"

LISTINGS_PER_RUN = 50

WATCHED_VEHICLES = [
    {
        "name": "G80 M3",
        "params": {
            "make": "BMW",
            "model": "M3",
            "year_range": "2021-2026",
            "car_type": "used",
        },
    },
    {
        "name": "C8 Corvette",
        "params": {
            "make": "Chevrolet",
            "model": "Corvette",
            "year_range": "2020-2026",
            "car_type": "used",
        },
    },
    {
        "name": "S550 Mustang",
        "params": {
            "make": "Ford",
            "model": "Mustang",
            "year_range": "2015-2023",
            "car_type": "used",
        },
    },
    {
        "name": "6th Gen Camaro",
        "params": {
            "make": "Chevrolet",
            "model": "Camaro",
            "year_range": "2016-2024",
            "car_type": "used",
        },
    },
]
# %%
def fetch_vehicle_data(vehicle_params, rows):
    """Single API call that gets both aggregate stats and a page of listings."""
    params = {
        "api_key": API_KEY,
        "rows": rows,
        "stats": "price,miles,dom_active",
        **vehicle_params,
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)

    if resp.status_code != 200:
        raise RuntimeError(
            f"Marketcheck API error {resp.status_code}: {resp.text[:500]}"
        )

    return resp.json()


tmp = fetch_vehicle_data(WATCHED_VEHICLES[1]["params"], LISTINGS_PER_RUN)
print(f"{len(tmp['listings'])=}")

# %%
tmp_miles = []
tmp_price = []
for x in range(len(tmp['listings'])):
    if "price" not in tmp['listings'][x].keys():
        continue
    if tmp['listings'][x]['build']['trim'] not in ['2LT', '3LT']:
    # if tmp['listings'][x]['build']['trim'] not in ["GT", "GT Premium"]:
        continue
    tmp_miles.append(tmp['listings'][x]['miles'])
    tmp_price.append(tmp['listings'][x]['price'])

plt.figure(figsize=(6,4))
plt.scatter(tmp_miles, tmp_price)
plt.xlabel('Miles')
plt.ylabel('Price')
plt.title('Price vs Mileage')


# %%
def fetch_vehicle_data_paginated(vehicle_params, total_rows_needed):
    all_listings = []
    page_size = 50  # Match the Free Tier limit per API request
    
    for start in range(0, total_rows_needed, page_size):
        params = {
            "api_key": API_KEY,
            "rows": min(page_size, total_rows_needed - start),
            "start": start,
            "stats": "price,miles,dom_active",
            **vehicle_params,
        }
        resp = requests.get(BASE_URL, params=params, timeout=30)
        
        if resp.status_code != 200:
            raise RuntimeError(f"Marketcheck API error {resp.status_code}: {resp.text[:500]}")
            
        data = resp.json()
        listings = data.get("listings", [])
        all_listings.extend(listings)
        
        # Stop early if no more listings are returned
        if not listings or len(listings) < page_size:
            break
            
    return all_listings

# Example: Fetch 50 total listings across 5 API calls
listings = fetch_vehicle_data_paginated(WATCHED_VEHICLES[1]["params"], 150)
print(f"Total retrieved: {len(listings)}")


# %%
tmp_miles = []
tmp_price = []
for x in range(len(listings)):
    if "price" not in listings[x].keys():
        continue
    if listings[x]['build']['trim'] not in ['2LT', '3LT']:
    # if tmp['listings'][x]['build']['trim'] not in ["GT", "GT Premium"]:
        continue
    tmp_miles.append(listings[x]['miles'])
    tmp_price.append(listings[x]['price'])

plt.figure(figsize=(6,4))
plt.scatter(tmp_miles, tmp_price)
plt.xlabel('Miles')
plt.ylabel('Price')
plt.title('Price vs Mileage')

# %%
def fetch_vehicle_trims(vehicle_params):
    make = vehicle_params["make"]
    model = vehicle_params["model"]
    params = {
        "api_key": API_KEY,
        "make": make,
        "model": model,
        "rows": 0,
        "facets": "trim|0|100|1",  # all trims with at least 1 listing
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    trims = data.get("facets", {}).get("trim", [])
    print(f"\nTrims found for {make} {model} ({data.get('num_found', 0)} total listings):\n")
    for t in trims:
        print(f"  {t['item']:<30} ({t['count']} listings)")
    return trims

tmp_trims = fetch_vehicle_trims(WATCHED_VEHICLES[1]["params"])
# %%

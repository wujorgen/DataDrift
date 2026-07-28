"""
Config for the car price tracker.

Add/edit entries in WATCHED_VEHICLES to change what gets tracked.
Each entry is a dict of Marketcheck search params - see
https://docs.marketcheck.com/docs/api/cars/inventory/inventory-search
for the full parameter list.

Tip: use scripts/discover_trims.py first to see exact trim strings
before locking them into year_range/trim filters here.
"""

import os

# Set this in your shell, e.g.:
#   export MARKETCHECK_API_KEY="your_key_here"
API_KEY = os.environ.get("MARKETCHECK_API_KEY")

BASE_URL = "https://api.marketcheck.com/v2/search/car/active"

DB_PATH = os.path.join(os.path.dirname(__file__), "car_prices.db")

# Each vehicle needs a unique "name" (used as the DB key) plus search filters.
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
]

# How many individual listings to store per run, per vehicle (max 50 per Marketcheck).
# Set to 0 if you only want the aggregate stats snapshot, not individual listings.
LISTINGS_PER_RUN = 50

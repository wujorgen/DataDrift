#!/usr/bin/env python3
"""
Run this periodically (e.g. weekly via cron) to snapshot current market
prices for your watched vehicles into a local SQLite database.

Usage:
    export MARKETCHECK_API_KEY="your_key_here"
    python3 track_prices.py

Cron example (every Monday at 9am):
    0 9 * * 1 cd /path/to/car_tracker && /usr/bin/python3 track_prices.py >> tracker.log 2>&1
"""

import sys
from datetime import datetime, timezone

import requests

from config import API_KEY, BASE_URL, WATCHED_VEHICLES, LISTINGS_PER_RUN
from db import get_conn, init_db, insert_snapshot, insert_listings


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


def run():
    if not API_KEY:
        print(
            "ERROR: MARKETCHECK_API_KEY is not set. "
            "Run: export MARKETCHECK_API_KEY='your_key_here'",
            file=sys.stderr,
        )
        sys.exit(1)

    init_db()
    run_at = datetime.now(timezone.utc).isoformat()

    with get_conn() as conn:
        for vehicle in WATCHED_VEHICLES:
            name = vehicle["name"]
            print(f"Fetching: {name} ...")

            try:
                data = fetch_vehicle_data(vehicle["params"], LISTINGS_PER_RUN)
            except Exception as e:
                print(f"  FAILED: {e}", file=sys.stderr)
                continue

            num_found = data.get("num_found", 0)
            stats = data.get("stats", {})
            listings = data.get("listings", [])

            insert_snapshot(
                conn,
                vehicle_name=name,
                run_at=run_at,
                num_found=num_found,
                price_stats=stats.get("price"),
                miles_stats=stats.get("miles"),
                dom_stats=stats.get("dom_active"),
            )

            if listings:
                insert_listings(conn, name, run_at, listings)

            price_mean = (stats.get("price") or {}).get("mean")
            price_str = f"${price_mean:,.0f}" if price_mean else "n/a"
            print(f"  {num_found} listings found | avg price: {price_str} | stored {len(listings)} listing rows")

    print(f"\nDone. Snapshot timestamp: {run_at}")


if __name__ == "__main__":
    run()

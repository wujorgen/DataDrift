#!/usr/bin/env python3
"""
One-off helper: shows the exact trim strings Marketcheck uses for a given
make/model, so you can filter precisely (e.g. separate Z06 from base Stingray)
instead of guessing spellings.

Usage:
    export MARKETCHECK_API_KEY="your_key_here"
    python3 discover_trims.py BMW M3
    python3 discover_trims.py Chevrolet Corvette
"""

import sys
import requests
from config import API_KEY, BASE_URL


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 discover_trims.py <make> <model>")
        sys.exit(1)

    make, model = sys.argv[1], sys.argv[2]

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


if __name__ == "__main__":
    main()

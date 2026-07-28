#!/usr/bin/env python3
"""
Print a quick summary of price history from the local database.

Usage:
    python3 report.py
"""

from db import get_conn


def main():
    with get_conn() as conn:
        vehicles = conn.execute(
            "SELECT DISTINCT vehicle_name FROM snapshots ORDER BY vehicle_name"
        ).fetchall()

        if not vehicles:
            print("No data yet. Run track_prices.py first.")
            return

        for v in vehicles:
            name = v["vehicle_name"]
            print(f"\n=== {name} ===")
            rows = conn.execute(
                """
                SELECT run_at, num_found, price_mean, price_median, price_min, price_max, miles_mean
                FROM snapshots
                WHERE vehicle_name = ?
                ORDER BY run_at
                """,
                (name,),
            ).fetchall()

            for r in rows:
                date = r["run_at"][:10]
                mean = f"${r['price_mean']:,.0f}" if r["price_mean"] else "n/a"
                median = f"${r['price_median']:,.0f}" if r["price_median"] else "n/a"
                lo = f"${r['price_min']:,.0f}" if r["price_min"] else "n/a"
                hi = f"${r['price_max']:,.0f}" if r["price_max"] else "n/a"
                miles = f"{r['miles_mean']:,.0f}mi" if r["miles_mean"] else "n/a"
                print(f"  {date} | n={r['num_found']:<5} | mean={mean:<10} median={median:<10} range=[{lo}-{hi}] avg_miles={miles}")

            if len(rows) >= 2:
                first, last = rows[0], rows[-1]
                if first["price_mean"] and last["price_mean"]:
                    delta = last["price_mean"] - first["price_mean"]
                    pct = (delta / first["price_mean"]) * 100
                    print(f"  --> Change since {first['run_at'][:10]}: {delta:+,.0f} ({pct:+.1f}%)")


if __name__ == "__main__":
    main()

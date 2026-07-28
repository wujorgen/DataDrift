"""
SQLite schema + helpers for the car price tracker.

Two tables:
  - snapshots: one row per (vehicle, run) with aggregate market stats
               (mean/median/min/max price and mileage, count of listings, days on market)
  - listings:  one row per (vehicle, run, listing) for individual cars seen that run,
               so you can also look at specific examples later, not just aggregates
"""

import sqlite3
from contextlib import contextmanager

from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_name TEXT NOT NULL,
    run_at TEXT NOT NULL,              -- ISO timestamp of when this snapshot was taken
    num_found INTEGER,                 -- total matching listings in the market

    price_mean REAL,
    price_median REAL,
    price_min REAL,
    price_max REAL,
    price_count INTEGER,

    miles_mean REAL,
    miles_median REAL,

    dom_active_mean REAL               -- avg days on market (active)
);

CREATE TABLE IF NOT EXISTS listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_name TEXT NOT NULL,
    run_at TEXT NOT NULL,
    vin TEXT,
    listing_id TEXT,
    price REAL,
    miles INTEGER,
    year INTEGER,
    trim TEXT,
    exterior_color TEXT,
    dealer_city TEXT,
    dealer_state TEXT,
    dom_active INTEGER,
    vdp_url TEXT
);

CREATE INDEX IF NOT EXISTS idx_snapshots_vehicle ON snapshots(vehicle_name, run_at);
CREATE INDEX IF NOT EXISTS idx_listings_vehicle ON listings(vehicle_name, run_at);
CREATE INDEX IF NOT EXISTS idx_listings_vin ON listings(vin);
"""


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.executescript(SCHEMA)


def insert_snapshot(conn, vehicle_name, run_at, num_found, price_stats, miles_stats, dom_stats):
    """price_stats/miles_stats/dom_stats are dicts as returned by Marketcheck's `stats` field,
    or None if not present."""
    conn.execute(
        """
        INSERT INTO snapshots (
            vehicle_name, run_at, num_found,
            price_mean, price_median, price_min, price_max, price_count,
            miles_mean, miles_median,
            dom_active_mean
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            vehicle_name,
            run_at,
            num_found,
            (price_stats or {}).get("mean"),
            (price_stats or {}).get("median"),
            (price_stats or {}).get("min"),
            (price_stats or {}).get("max"),
            (price_stats or {}).get("count"),
            (miles_stats or {}).get("mean"),
            (miles_stats or {}).get("median"),
            (dom_stats or {}).get("mean"),
        ),
    )


def insert_listings(conn, vehicle_name, run_at, listings):
    rows = []
    for l in listings:
        build = l.get("build", {}) or {}
        dealer = l.get("dealer", {}) or {}
        rows.append(
            (
                vehicle_name,
                run_at,
                l.get("vin"),
                l.get("id"),
                l.get("price"),
                l.get("miles"),
                build.get("year"),
                build.get("trim"),
                l.get("exterior_color"),
                dealer.get("city"),
                dealer.get("state"),
                l.get("dom_active"),
                l.get("vdp_url"),
            )
        )
    conn.executemany(
        """
        INSERT INTO listings (
            vehicle_name, run_at, vin, listing_id, price, miles, year, trim,
            exterior_color, dealer_city, dealer_state, dom_active, vdp_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )

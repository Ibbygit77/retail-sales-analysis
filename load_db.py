"""Load the CSV files in data/ into a SQLite database called sales.db."""

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent
DB = ROOT / "sales.db"

SCHEMA = """
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS stores;

CREATE TABLE stores (
    store_id   INTEGER PRIMARY KEY,
    store_name TEXT NOT NULL,
    city       TEXT NOT NULL,
    state      TEXT NOT NULL
);

CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT NOT NULL,
    unit_cost    REAL NOT NULL,
    unit_price   REAL NOT NULL
);

CREATE TABLE orders (
    order_id   INTEGER PRIMARY KEY,
    order_date TEXT NOT NULL,          -- YYYY-MM-DD
    store_id   INTEGER NOT NULL REFERENCES stores(store_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity   INTEGER NOT NULL,
    discount   REAL NOT NULL           -- 0.1 means 10% off
);
"""


def load(conn, table, filename):
    with open(ROOT / "data" / filename, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        marks = ", ".join("?" for _ in header)
        conn.executemany(f"INSERT INTO {table} VALUES ({marks})", reader)


def main():
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    load(conn, "stores", "stores.csv")
    load(conn, "products", "products.csv")
    load(conn, "orders", "orders.csv")
    conn.commit()
    for table in ("stores", "products", "orders"):
        n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {n} rows")
    conn.close()
    print(f"Database ready: {DB.name}")


if __name__ == "__main__":
    main()

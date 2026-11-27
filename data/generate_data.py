"""Generate a synthetic retail sales dataset for Harbour & Co. (fictional).

Uses only the Python standard library. The random seed is fixed, so everyone
who runs this gets exactly the same data.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
OUT = Path(__file__).parent

STORES = [
    (1, "Sydney CBD", "Sydney", "NSW"),
    (2, "Parramatta", "Sydney", "NSW"),
    (3, "Macquarie Park", "Sydney", "NSW"),
    (4, "Melbourne Central", "Melbourne", "VIC"),
    (5, "Chadstone", "Melbourne", "VIC"),
    (6, "Geelong", "Geelong", "VIC"),
    (7, "Brisbane City", "Brisbane", "QLD"),
    (8, "Gold Coast", "Gold Coast", "QLD"),
    (9, "Perth City", "Perth", "WA"),
    (10, "Fremantle", "Perth", "WA"),
    (11, "Adelaide City", "Adelaide", "SA"),
    (12, "Glenelg", "Adelaide", "SA"),
]

# category: [(product name, unit cost, unit price)]
CATALOGUE = {
    "Electronics": [
        ("Wireless Earbuds", 45, 99), ("Bluetooth Speaker", 38, 79),
        ("Phone Charger", 6, 25), ("Smart Watch", 120, 249),
        ("Laptop Stand", 18, 49), ("USB-C Hub", 22, 59),
        ("Webcam HD", 30, 69), ("Power Bank", 15, 45),
    ],
    "Home": [
        ("Scented Candle", 4, 19), ("Throw Blanket", 20, 59),
        ("Ceramic Vase", 9, 35), ("Desk Lamp", 16, 45),
        ("Cushion Cover", 5, 22), ("Wall Clock", 12, 39),
        ("Photo Frame", 3, 15), ("Storage Basket", 8, 29),
    ],
    "Kitchen": [
        ("Coffee Grinder", 28, 79), ("Chef Knife", 25, 89),
        ("Cutting Board", 7, 29), ("Water Bottle", 6, 29),
        ("French Press", 14, 45), ("Mixing Bowls", 10, 35),
        ("Tea Infuser", 2, 12), ("Cast Iron Pan", 30, 99),
    ],
    "Outdoor": [
        ("Picnic Rug", 12, 45), ("Camping Chair", 22, 69),
        ("Insulated Cooler", 35, 119), ("Beach Towel", 8, 32),
        ("Hiking Backpack", 40, 129), ("Head Torch", 9, 35),
        ("Sun Umbrella", 18, 59), ("Drink Flask", 7, 29),
    ],
    "Stationery": [
        ("Notebook A5", 2, 12), ("Fountain Pen", 15, 49),
        ("Desk Planner", 6, 25), ("Highlighter Set", 2, 9),
        ("Leather Folio", 20, 69), ("Sticky Notes", 1, 6),
        ("Pencil Case", 4, 18), ("Gel Pen Pack", 3, 14),
    ],
}

# Seasonal demand multiplier by month (Jan..Dec): Christmas peak, winter dip.
SEASON = [0.9, 0.8, 0.9, 0.95, 1.0, 0.85, 0.85, 0.9, 1.0, 1.05, 1.3, 1.7]
# Some stores are busier than others.
STORE_WEIGHT = {1: 1.6, 2: 1.0, 3: 1.1, 4: 1.5, 5: 1.4, 6: 0.6,
                7: 1.2, 8: 0.9, 9: 1.0, 10: 0.7, 11: 0.9, 12: 0.6}
# Outdoor sells more in summer, Electronics more at Christmas.
CATEGORY_MONTH_BOOST = {"Outdoor": {12: 1.6, 1: 1.6, 2: 1.4},
                        "Electronics": {11: 1.3, 12: 1.6}}


def main():
    products = []
    pid = 1
    for category, items in CATALOGUE.items():
        for name, cost, price in items:
            products.append((pid, name, category, cost, price))
            pid += 1

    with open(OUT / "stores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["store_id", "store_name", "city", "state"])
        w.writerows(STORES)

    with open(OUT / "products.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["product_id", "product_name", "category",
                    "unit_cost", "unit_price"])
        w.writerows(products)

    start, end = date(2024, 1, 1), date(2025, 12, 31)
    order_id = 100000
    rows = []
    day = start
    while day <= end:
        weekend = 1.3 if day.weekday() >= 5 else 1.0
        base = 26 * SEASON[day.month - 1] * weekend
        for _ in range(int(random.gauss(base, base * 0.15))):
            store_id = random.choices(list(STORE_WEIGHT),
                                      weights=list(STORE_WEIGHT.values()))[0]
            weights = [CATEGORY_MONTH_BOOST.get(p[2], {}).get(day.month, 1.0)
                       for p in products]
            product = random.choices(products, weights=weights)[0]
            quantity = random.choices([1, 2, 3, 4, 5],
                                      weights=[55, 25, 10, 6, 4])[0]
            discount = random.choices([0, 0.1, 0.2, 0.3],
                                      weights=[70, 15, 10, 5])[0]
            # Discounts nudge quantity up a little.
            if discount and random.random() < discount * 2:
                quantity += 1
            order_id += 1
            rows.append((order_id, day.isoformat(), store_id, product[0],
                         quantity, discount))
        day += timedelta(days=1)

    with open(OUT / "orders.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["order_id", "order_date", "store_id", "product_id",
                    "quantity", "discount"])
        w.writerows(rows)

    print(f"Wrote {len(STORES)} stores, {len(products)} products, "
          f"{len(rows)} order lines to {OUT}")


if __name__ == "__main__":
    main()

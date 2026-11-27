"""Run the analysis queries and save the results for the web dashboard.

Output: docs/data.js  (loaded by docs/index.html)
Run after load_db.py:  python build_dashboard_data.py
"""

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs" / "data.js"

SALES_VIEW = """
CREATE TEMP VIEW sales AS
SELECT o.order_date,
       strftime('%Y', o.order_date)    AS year,
       strftime('%Y-%m', o.order_date) AS month,
       s.store_name, s.city, s.state, p.product_name, p.category,
       o.quantity, o.discount,
       o.quantity * p.unit_price * (1 - o.discount) AS revenue,
       o.quantity * p.unit_price * (1 - o.discount) - o.quantity * p.unit_cost AS profit
FROM orders o
JOIN stores s   ON s.store_id   = o.store_id
JOIN products p ON p.product_id = o.product_id
"""


def rows(conn, sql, params=()):
    cur = conn.execute(sql, params)
    names = [d[0] for d in cur.description]
    return [dict(zip(names, r)) for r in cur.fetchall()]


def summary(conn, where, params):
    q = lambda sql: rows(conn, sql.format(where=where), params)
    return {
        "kpi": q("""
            SELECT ROUND(SUM(revenue)) AS revenue, ROUND(SUM(profit)) AS profit,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin,
                   SUM(quantity) AS units, COUNT(*) AS lines
            FROM sales WHERE {where}""")[0],
        "monthly": q("""
            SELECT month, ROUND(SUM(revenue)) AS revenue, ROUND(SUM(profit)) AS profit
            FROM sales WHERE {where} GROUP BY month ORDER BY month"""),
        "category": q("""
            SELECT category AS name, ROUND(SUM(revenue)) AS revenue,
                   ROUND(SUM(profit)) AS profit,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin
            FROM sales WHERE {where} GROUP BY category ORDER BY revenue DESC"""),
        "cat_month": q("""
            SELECT category, CAST(strftime('%m', order_date) AS INTEGER) AS mo,
                   ROUND(SUM(revenue)) AS revenue
            FROM sales WHERE {where} GROUP BY category, mo ORDER BY category, mo"""),
        "state": q("""
            SELECT state AS name, COUNT(DISTINCT store_name) AS stores,
                   ROUND(SUM(revenue)) AS revenue, ROUND(SUM(profit)) AS profit,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin
            FROM sales WHERE {where} GROUP BY state ORDER BY revenue DESC"""),
        "stores": q("""
            SELECT store_name AS name, city, state, ROUND(SUM(revenue)) AS revenue,
                   ROUND(SUM(profit)) AS profit,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin
            FROM sales WHERE {where} GROUP BY store_name, city, state
            ORDER BY revenue DESC"""),
        "products": q("""
            SELECT product_name AS name, category, ROUND(SUM(revenue)) AS revenue,
                   SUM(quantity) AS units,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin
            FROM sales WHERE {where} GROUP BY product_name, category
            ORDER BY revenue DESC LIMIT 10"""),
        "weekday": q("""
            SELECT CAST(strftime('%w', order_date) AS INTEGER) AS dow,
                   ROUND(SUM(revenue) / COUNT(DISTINCT order_date)) AS revenue_per_day
            FROM sales WHERE {where} GROUP BY dow ORDER BY dow"""),
        "discount": q("""
            SELECT CAST(ROUND(discount * 100) AS INTEGER) AS pct, COUNT(*) AS lines,
                   ROUND(AVG(quantity), 2) AS units, ROUND(AVG(profit), 2) AS profit,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin
            FROM sales WHERE {where} GROUP BY discount ORDER BY discount"""),
    }


def main():
    conn = sqlite3.connect(ROOT / "sales.db")
    conn.execute(SALES_VIEW)
    years = [r["year"] for r in rows(conn, "SELECT DISTINCT year FROM sales ORDER BY year")]
    data = {"All": summary(conn, "1 = 1", ())}
    for y in years:
        data[y] = summary(conn, "year = ?", (y,))
    conn.close()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("window.DASHBOARD_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n",
                   encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} for periods: {', '.join(data)}")


if __name__ == "__main__":
    main()

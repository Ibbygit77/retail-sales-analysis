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
SELECT strftime('%Y', o.order_date)    AS year,
       strftime('%Y-%m', o.order_date) AS month,
       s.store_name, s.state, p.product_name, p.category,
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
    return {
        "kpi": rows(conn, f"""
            SELECT ROUND(SUM(revenue)) AS revenue, ROUND(SUM(profit)) AS profit,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin,
                   SUM(quantity) AS units, COUNT(*) AS lines
            FROM sales WHERE {where}""", params)[0],
        "monthly": rows(conn, f"""
            SELECT month, ROUND(SUM(revenue)) AS revenue, ROUND(SUM(profit)) AS profit
            FROM sales WHERE {where} GROUP BY month ORDER BY month""", params),
        "category": rows(conn, f"""
            SELECT category AS name, ROUND(SUM(revenue)) AS revenue,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin
            FROM sales WHERE {where} GROUP BY category ORDER BY revenue DESC""", params),
        "state": rows(conn, f"""
            SELECT state AS name, ROUND(SUM(revenue)) AS revenue,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin
            FROM sales WHERE {where} GROUP BY state ORDER BY revenue DESC""", params),
        "products": rows(conn, f"""
            SELECT product_name AS name, category, ROUND(SUM(revenue)) AS revenue,
                   SUM(quantity) AS units
            FROM sales WHERE {where} GROUP BY product_name, category
            ORDER BY revenue DESC LIMIT 10""", params),
        "stores": rows(conn, f"""
            SELECT store_name AS name, state, ROUND(SUM(revenue)) AS revenue,
                   ROUND(SUM(profit)) AS profit,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin
            FROM sales WHERE {where} GROUP BY store_name, state ORDER BY revenue DESC""", params),
        "discount": rows(conn, f"""
            SELECT CAST(ROUND(discount * 100) AS INTEGER) AS pct, COUNT(*) AS lines,
                   ROUND(AVG(quantity), 2) AS units, ROUND(AVG(profit), 2) AS profit,
                   ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin
            FROM sales WHERE {where} GROUP BY discount ORDER BY discount""", params),
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
    OUT.write_text("window.DASHBOARD_DATA = " + json.dumps(data, indent=1) + ";\n",
                   encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} for periods: {', '.join(data)}")


if __name__ == "__main__":
    main()

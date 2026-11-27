-- ============================================================
-- 02 Revenue and profit: where does the money come from?
--   revenue = quantity * unit_price * (1 - discount)
--   profit  = revenue - quantity * unit_cost
-- ============================================================

-- A reusable view that joins the three tables and calculates the money columns.
DROP VIEW IF EXISTS sales;
CREATE VIEW sales AS
SELECT o.order_id,
       o.order_date,
       strftime('%Y', o.order_date)    AS year,
       strftime('%Y-%m', o.order_date) AS month,
       s.store_name, s.state,
       p.product_name, p.category,
       o.quantity, o.discount,
       o.quantity * p.unit_price * (1 - o.discount)                         AS revenue,
       o.quantity * p.unit_price * (1 - o.discount) - o.quantity * p.unit_cost AS profit
FROM orders o
JOIN stores   s ON s.store_id   = o.store_id
JOIN products p ON p.product_id = o.product_id;

-- Headline numbers by year
SELECT year,
       ROUND(SUM(revenue))                      AS revenue,
       ROUND(SUM(profit))                       AS profit,
       ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin_pct,
       SUM(quantity)                            AS units
FROM sales
GROUP BY year;

-- Revenue and margin by category
SELECT category,
       ROUND(SUM(revenue))                        AS revenue,
       ROUND(SUM(profit))                         AS profit,
       ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin_pct
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- Revenue by state
SELECT state,
       ROUND(SUM(revenue)) AS revenue,
       ROUND(SUM(profit))  AS profit
FROM sales
GROUP BY state
ORDER BY revenue DESC;

-- Store league table
SELECT store_name, state,
       ROUND(SUM(revenue))                        AS revenue,
       ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin_pct
FROM sales
GROUP BY store_name, state
ORDER BY revenue DESC;

-- Top 10 products by revenue
SELECT product_name, category,
       ROUND(SUM(revenue)) AS revenue,
       SUM(quantity)       AS units
FROM sales
GROUP BY product_name, category
ORDER BY revenue DESC
LIMIT 10;

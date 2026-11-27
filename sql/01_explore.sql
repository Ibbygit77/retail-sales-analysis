-- ============================================================
-- 01 Explore the data
-- Run with:  python run_query.py sql/01_explore.sql
-- ============================================================

-- First rows of each table
SELECT * FROM stores LIMIT 5;
SELECT * FROM products LIMIT 5;
SELECT * FROM orders LIMIT 5;

-- How many order lines, and what period do they cover?
SELECT COUNT(*)        AS order_lines,
       MIN(order_date) AS first_day,
       MAX(order_date) AS last_day
FROM orders;

-- How many products are in each category?
SELECT category, COUNT(*) AS products
FROM products
GROUP BY category
ORDER BY category;

-- Stores per state
SELECT state, COUNT(*) AS stores
FROM stores
GROUP BY state
ORDER BY stores DESC;

-- Share of order lines sold at a discount
SELECT ROUND(100.0 * SUM(discount > 0) / COUNT(*), 1) AS pct_discounted
FROM orders;

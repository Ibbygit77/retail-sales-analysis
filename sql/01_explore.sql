-- ============================================================
-- Step 1: Explore the data
-- Run with:  python run_query.py sql/01_explore.sql
-- ============================================================

-- Example 1: look at the first 10 rows of each table.
SELECT * FROM stores LIMIT 10;
SELECT * FROM products LIMIT 10;
SELECT * FROM orders LIMIT 10;

-- Example 2: how many order lines are there?
SELECT COUNT(*) AS order_lines FROM orders;

-- Example 3: what date range does the data cover?
SELECT MIN(order_date) AS first_day, MAX(order_date) AS last_day FROM orders;


-- ============================================================
-- YOUR TURN — write a query under each question, then run the file.
-- Hints are in STEPS.md. Delete the "SELECT 'todo'" line when you start.
-- ============================================================

-- Q1. How many products are in each category?
--     (hint: GROUP BY category)
SELECT 'todo Q1';

-- Q2. List all stores in NSW.
--     (hint: WHERE state = 'NSW')
SELECT 'todo Q2';

-- Q3. What are the 5 most expensive products by unit_price?
--     (hint: ORDER BY ... DESC LIMIT 5)
SELECT 'todo Q3';

-- Q4. How many order lines had a discount (discount > 0)?
SELECT 'todo Q4';

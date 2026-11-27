-- ============================================================
-- 04 Seasonality by category and trading patterns by weekday
-- (uses the "sales" view created in 02_revenue.sql - run that first)
-- ============================================================

-- Revenue by category and calendar month (both years combined)
SELECT category,
       strftime('%m', order_date) AS month_no,
       ROUND(SUM(revenue))        AS revenue
FROM sales
GROUP BY category, month_no
ORDER BY category, month_no;

-- Each month compared with the category's average month (1.00 = a normal month)
WITH cm AS (
    SELECT category, strftime('%m', order_date) AS month_no, SUM(revenue) AS revenue
    FROM sales
    GROUP BY category, month_no
)
SELECT category, month_no,
       ROUND(revenue / AVG(revenue) OVER (PARTITION BY category), 2) AS index_vs_avg
FROM cm
ORDER BY index_vs_avg DESC
LIMIT 10;

-- Average revenue per trading day, by weekday (0 = Sunday, 6 = Saturday)
SELECT strftime('%w', order_date)                        AS weekday_no,
       ROUND(SUM(revenue) / COUNT(DISTINCT order_date))  AS revenue_per_day
FROM sales
GROUP BY weekday_no
ORDER BY weekday_no;

-- Weekend vs weekday revenue per day
SELECT CASE WHEN strftime('%w', order_date) IN ('0', '6') THEN 'Weekend' ELSE 'Weekday' END AS day_type,
       ROUND(SUM(revenue) / COUNT(DISTINCT order_date)) AS revenue_per_day
FROM sales
GROUP BY day_type;

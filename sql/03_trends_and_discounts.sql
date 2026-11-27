-- ============================================================
-- 03 Trends over time and the effect of discounts
-- (uses the "sales" view created in 02_revenue.sql - run that first)
-- ============================================================

-- Monthly revenue
SELECT month,
       ROUND(SUM(revenue)) AS revenue,
       ROUND(SUM(profit))  AS profit
FROM sales
GROUP BY month
ORDER BY month;

-- Which calendar months are strongest? (average across both years)
SELECT strftime('%m', order_date)        AS month_no,
       ROUND(SUM(revenue) / 2)           AS avg_revenue
FROM sales
GROUP BY month_no
ORDER BY avg_revenue DESC;

-- Outdoor products: summer vs the rest of the year
SELECT CASE WHEN strftime('%m', order_date) IN ('12','01','02')
            THEN 'Summer (Dec-Feb)' ELSE 'Rest of year' END AS season,
       ROUND(SUM(revenue) / COUNT(DISTINCT month)) AS revenue_per_month
FROM sales
WHERE category = 'Outdoor'
GROUP BY season;

-- Discounts: do they pay for themselves?
SELECT CAST(ROUND(discount * 100) AS INTEGER) || '%' AS discount,
       COUNT(*)                                   AS order_lines,
       ROUND(AVG(quantity), 2)                    AS avg_units,
       ROUND(AVG(revenue), 2)                     AS avg_revenue,
       ROUND(AVG(profit), 2)                      AS avg_profit,
       ROUND(100 * SUM(profit) / SUM(revenue), 1) AS margin_pct
FROM sales
GROUP BY discount
ORDER BY discount;

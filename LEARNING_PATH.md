# Learning path

This project was built with an AI coding assistant while I learn. My goal is to understand every file well enough to explain it in an interview and to rebuild the analysis myself. I tick each step off as I finish it.

## Stage 1 — SQL basics
- [ ] SQLBolt lessons 1–4: `SELECT`, `WHERE`, `ORDER BY`, `LIMIT` → https://sqlbolt.com/
- [ ] SQLBolt lessons 10–11: `COUNT`, `SUM`, `GROUP BY`
- [ ] Run `python run_query.py sql/01_explore.sql` and explain each query out loud
- [ ] Write my own queries in `practice/my_queries.sql`:
  - How many stores are in each state?
  - What are the 5 cheapest products?
  - How many order lines had more than 3 units?

## Stage 2 — Joins and calculations
- [ ] SQLBolt lessons 6–7: `JOIN`
- [ ] Explain the `sales` view in `sql/02_revenue.sql` line by line
- [ ] Without looking: write a query for revenue by category

## Stage 3 — Trends and business insight
- [ ] Explain `strftime('%Y-%m', order_date)` and why it groups by month
- [ ] Re-check each of the 5 insights in the README against the query results
- [ ] Write one new insight of my own (e.g. which store has the lowest margin, and why might that be?)

## Stage 4 — Rebuild the dashboard in Power BI (supports the PL-300 certification)
- [ ] Install Power BI Desktop (free, Microsoft Store)
- [ ] Import the three CSV files from `data/` and create relationships
- [ ] Create measures in DAX: Revenue, Profit, Margin %
- [ ] Build: KPI cards, monthly revenue line, revenue by category, a slicer for year
- [ ] Save as `powerbi/harbour-sales.pbix` and add a screenshot to the README

## Stage 5 — Python
- [ ] Explain what `load_db.py` does, step by step
- [ ] Change `generate_data.py` to add a sixth product category, rerun everything, and see the dashboard update

## Interview prep
- [ ] Practise a 2-minute walkthrough: business question → data → SQL → insight → recommendation
- [ ] Be ready to answer: "What would you do next with this data?"

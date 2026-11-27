# Project steps

Tick each box as you finish it (change `[ ]` to `[x]`), then commit and push — your GitHub history becomes proof of steady progress.

## Stage 1 — Explore the data with SQL (Week 1)
- [ ] Learn SQL basics: `SELECT`, `WHERE`, `ORDER BY`, `LIMIT` → [SQLBolt lessons 1–4](https://sqlbolt.com/)
- [ ] Learn `COUNT`, `GROUP BY` → SQLBolt lessons 10–11
- [ ] Run `python run_query.py sql/01_explore.sql` and read the example results
- [ ] Answer Q1–Q4 in `sql/01_explore.sql`
- [ ] Commit: `git add . ; git commit -m "Answer exploration questions" ; git push`

**Hints**
- Q1: `SELECT category, COUNT(*) AS products FROM products GROUP BY category;`
  (try writing it yourself first!)
- Q3: sort descending with `ORDER BY unit_price DESC`

## Stage 2 — Join tables and calculate revenue (Week 2)
- [ ] Learn `JOIN` → SQLBolt lessons 6–7
- [ ] Revenue for one order line = `quantity * unit_price * (1 - discount)`
- [ ] Profit = revenue − `quantity * unit_cost`
- [ ] Create `sql/02_revenue.sql`: total revenue and profit by category, by state, by store

## Stage 3 — Trends over time (Week 3)
- [ ] Monthly revenue: `strftime('%Y-%m', order_date)`
- [ ] Which months are strongest? Is there a Christmas peak?
- [ ] Do discounted orders make more or less profit per order?
- [ ] Write findings in the **Key insights** section of README.md

## Stage 4 — Power BI dashboard (Weeks 4–6)
- [ ] Install Power BI Desktop (free, from the Microsoft Store)
- [ ] Import the three CSV files and create relationships
- [ ] Build: revenue KPI cards, monthly trend line, revenue by category, map by state
- [ ] Save the `.pbix` in a `dashboard/` folder and add a screenshot to README.md

## Stage 5 — Polish (end of Week 6)
- [ ] Rewrite the README insights as short, business-style bullet points
- [ ] Update your GitHub profile README: change status to ✅ Complete
- [ ] Add the project to your CV and LinkedIn

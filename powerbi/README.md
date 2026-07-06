# Power BI Dashboard: UAE SME Analytics

## Data Source
- BigQuery dataset: `analytics`
- Main table: `fct_sme_performance` (25,800 rows)

## Dashboard Visuals
| # | Visual | Type | Purpose |
|---|--------|------|---------|
| 1 | Revenue by Emirate | Bar Chart | Show top emirates |
| 2 | Industry Performance | Column Chart | Compare industries |
| 3 | Online vs Offline Mix | Donut Chart | Digital adoption |
| 4 | Churn by Industry | Bar Chart | Retention issues |
| 5 | ROI vs Digital | Scatter Chart | Correlation analysis |
| 6 | Revenue Trend | Line Chart | Monthly growth |
| 7 | Employee Efficiency | Bar Chart | Revenue per employee |

## DAX Measures Created
- `Total_Revenue`
- `Avg_Churn_Rate`
- `Online_Penetration`
- `Rev_per_Employee`
- `YoY_Growth`
- `Marketing_Efficiency`

## How to Connect
1. Open Power BI Desktop
2. Get Data → Google BigQuery
3. Connect to project: `uae-sme-analytics-pipeline`
4. Select dataset: `analytics`
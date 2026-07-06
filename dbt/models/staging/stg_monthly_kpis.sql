WITH source AS (
    SELECT * FROM {{ source('raw_zone', 'monthly_kpis') }}
)

SELECT
    sme_id,
    DATE(month) AS month_date,
    revenue_aed,
    orders,
    online_sales_pct,
    avg_order_value,
    marketing_spend_aed,
    staff_count,
    new_customers,
    returning_customers,
    churn_rate,
    SAFE_DIVIDE(marketing_spend_aed, revenue_aed) AS marketing_roi_pct,
    SAFE_DIVIDE(orders, staff_count) AS orders_per_employee,
    SAFE_DIVIDE(new_customers, returning_customers) AS new_to_returning_ratio
FROM source
WHERE revenue_aed IS NOT NULL

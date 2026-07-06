WITH monthly AS (
    SELECT * FROM {{ ref('stg_monthly_kpis') }}
),
profiles AS (
    SELECT * FROM {{ ref('stg_sme_profiles') }}
)

SELECT
    monthly.sme_id,
    monthly.month_date,
    profiles.emirate,
    profiles.industry,
    profiles.subindustry,
    profiles.license_type,
    profiles.owner_nationality_group,
    profiles.employees,
    profiles.company_age_years,
    profiles.digital_adoption_score,
    profiles.female_owned,
    profiles.exporter,
    monthly.revenue_aed,
    monthly.orders,
    monthly.online_sales_pct,
    monthly.avg_order_value,
    monthly.marketing_spend_aed,
    monthly.marketing_roi_pct,
    monthly.new_customers,
    monthly.returning_customers,
    monthly.churn_rate,
    monthly.orders_per_employee,
    monthly.new_to_returning_ratio,
    EXTRACT(YEAR FROM monthly.month_date) AS year,
    EXTRACT(QUARTER FROM monthly.month_date) AS quarter,
    FORMAT_DATE('%Y-%m', monthly.month_date) AS year_month
FROM monthly
LEFT JOIN profiles ON monthly.sme_id = profiles.sme_id
WHERE monthly.revenue_aed > 0

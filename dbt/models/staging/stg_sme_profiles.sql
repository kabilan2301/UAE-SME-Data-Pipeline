WITH source AS (
    SELECT * FROM {{ source('raw_zone', 'sme_profiles') }}
)

SELECT
    sme_id,
    emirate,
    industry,
    subindustry,
    employees,
    annual_revenue_aed,
    founded_year,
    license_type,
    trade_license_issuer,
    owner_nationality_group,
    female_owned,
    exporter,
    digital_adoption_score,
    EXTRACT(YEAR FROM CURRENT_DATE()) - founded_year AS company_age_years,
    SAFE_DIVIDE(annual_revenue_aed, employees) AS revenue_per_employee
FROM source

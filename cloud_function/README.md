# Cloud Function: UAE SME Data Loader

## Purpose
This Cloud Function (2nd gen) downloads Excel files from a GitHub repository and loads them into BigQuery.

## Trigger
- HTTP trigger
- Scheduled daily at 6 AM UAE time via Cloud Scheduler

## Files Loaded
| Table | Rows | Description |
|-------|------|-------------|
| sme_profiles | 600 | Company profiles |
| monthly_kpis | 25,800 | Monthly performance metrics |
| macro_indicators | 55 | Economic indicators (PMI, oil price) |
| policy_events | 6 | Government policy events |
| kpi_mapping | 5 | Vision 2030 KPI definitions |

## Deployment Command
```bash
gcloud functions deploy load-revenue-fn-v3 \
    --gen2 \
    --region=us-central1 \
    --runtime=python311 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point=load_sme_data \
    --source=. \
    --memory=1024MB \
    --timeout=540s
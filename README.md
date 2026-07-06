# UAE SME Data Pipeline

## Overview

An end-to-end data pipeline that ingests, transforms, and visualizes UAE SME data using Google Cloud Platform, dbt, and Power BI.

## Architecture

Cloud Scheduler (6 AM UAE)
│
>
Cloud Function (load_sme_data)
│
>
BigQuery (raw_zone)
│
>
dbt Transformations
│
>
BigQuery (analytics)
│
>
Power BI Dashboard

## Technologies Used

| Component       | Technology                |
| --------------- | ------------------------- |
| Cloud Provider  | Google Cloud Platform     |
| Compute         | Cloud Functions (2nd Gen) |
| Data Warehouse  | BigQuery                  |
| Transformation  | dbt (Core)                |
| Orchestration   | Cloud Scheduler           |
| Visualization   | Power BI                  |
| Version Control | GitHub                    |

## Dataset

**Source:** UAE SME Growth Analysis Dataset  
**Files Loaded:** 5 Excel files, 26,466 total rows

| Table            | Rows   |
| ---------------- | ------ |
| sme_profiles     | 600    |
| monthly_kpis     | 25,800 |
| macro_indicators | 55     |
| policy_events    | 6      |
| kpi_mapping      | 5      |

## 🔐 IAM (Identity and Access Management)

The project uses the following IAM roles for secure access:

### Service Account

- **Runtime Identity**: The default Compute Engine service account `6167885285-compute@developer.gserviceaccount.com` was used as the runtime identity for the Cloud Function.

### Roles Assigned

| Role                        | Purpose                                             | Granted To                                                    |
| --------------------------- | --------------------------------------------------- | ------------------------------------------------------------- |
| `roles/bigquery.dataEditor` | Write data to BigQuery tables (`raw_zone` dataset)  | Service Account                                               |
| `roles/bigquery.jobUser`    | Create and run BigQuery load jobs                   | Service Account                                               |
| `roles/run.invoker`         | Allow Cloud Scheduler to trigger the Cloud Function | Service Account (or `allUsers` via `--allow-unauthenticated`) |

### Important

Without these IAM bindings, the Cloud Function would throw **permission denied** errors when trying to write to BigQuery or when Cloud Scheduler tried to trigger it. These roles enable secure, automated data ingestion.

## ⏰ Cloud Scheduler - Orchestration

The pipeline is fully automated using **Cloud Scheduler** to run the data ingestion function daily.

### Job Configuration

| Parameter          | Value                                                                          |
| ------------------ | ------------------------------------------------------------------------------ |
| **Name**           | `daily-sme-data-load`                                                          |
| **Frequency**      | `0 6 * * *` (Daily at 6:00 AM)                                                 |
| **Time Zone**      | `Asia/Dubai` (UAE local time)                                                  |
| **Target**         | `HTTP`                                                                         |
| **URL**            | Cloud Function HTTP endpoint: ` https://load-revenue-fn-v3-xdiugtyo2q-uc.a.run.app` |
| **Authentication** | `--allow-unauthenticated` (simplified for testing)                             |

### Project Flow

1. Cloud Scheduler sends an HTTP request to the Cloud Function URL at 6 AM daily
2. The Cloud Function downloads fresh Excel files from GitHub
3. Data is loaded into BigQuery `raw_zone` tables
4. dbt transformations update the `analytics` dataset

### Why Cloud Scheduler Was Chosen

- **Reliability**: Fully-managed service with guaranteed execution
- **Simplicity**: No need to manage cron servers
- **Cost-effective**: Minimal cost for daily triggers
- **Time-zone aware**: Configured for UAE business hours

### Deployment Command

``` bash
gcloud scheduler jobs create http daily-sme-data-load \
    --location=us-central1 \
    --schedule="0 6 * * *" \
    --time-zone="Asia/Dubai" \
    --uri=" https://load-revenue-fn-v3-xdiugtyo2q-uc.a.run.app" \
    --http-method=GET
```

### Key Features

1. Automated daily data ingestion via Cloud Scheduler

2. Production-grade dbt transformations

3. Interactive Power BI dashboard with 7 visuals

4. End-to-end pipeline from raw data to business insights

### Dashboard Visuals

1. Revenue by Emirate

2. Industry Performance

3. Online vs Offline Sales Mix

4. Churn Rate by Industry

5. ROI vs Digital Adoption

6. Revenue Trend Over Time

7. Employee Efficiency by Industry


### Project Set-up
### 1. GCP Setup

```bash
# Enable APIs
gcloud services enable bigquery.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
```


### 2. Deploy Cloud Function

```bash
cd cloud_function
gcloud functions deploy load-revenue-fn-v3 \
    --gen2 --region=us-central1 --runtime=python311 \
    --trigger-http --allow-unauthenticated \
    --entry-point=load_sme_data --source=. \
    --memory=1024MB --timeout=540s
```

### 3. Set Up IAM Permissions

```bash
# Grant BigQuery permissions to service account
gcloud projects add-iam-policy-binding uae-sme-analytics-pipeline \
    --member="serviceAccount:6167885285-compute@developer.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding uae-sme-analytics-pipeline \
    --member="serviceAccount:6167885285-compute@developer.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"
```

### 4. Configure Cloud Scheduler

```bash
gcloud scheduler jobs create http daily-sme-data-load \
    --location=us-central1 \
    --schedule="0 6 * * *" \
    --time-zone="Asia/Dubai" \
    --uri=" https://load-revenue-fn-v3-xdiugtyo2q-uc.a.run.app" \
    --http-method=GET
```


### 5. Run dbt Transformations

```bash
cd dbt
dbt clean
dbt run
```

### 6. Power BI

Open Power BI Desktop

Connect to BigQuery (analytics dataset)

Open powerbi/UAE_SME_Dashboard.pbix

### IAM Requirements

# Grant BigQuery permissions
```bash
gcloud projects add-iam-policy-binding uae-sme-analytics-pipeline \
    --member="serviceAccount:6167885285-compute@developer.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding uae-sme-analytics-pipeline \
    --member="serviceAccount:6167885285-compute@developer.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"
```

### Required Roles
Role | Purpose
roles/bigquery.dataEditor |	Write data to raw_zone tables
roles/bigquery.jobUser |	Create and run BigQuery load jobs
roles/run.invoker |	Allow HTTP invocation (for Cloud Scheduler)

### Trigger Configuration
```bash
gcloud scheduler jobs create http daily-sme-data-load \
    --location=us-central1 \
    --schedule="0 6 * * *" \
    --time-zone="Asia/Dubai" \
    --uri=" https://load-revenue-fn-v3-xdiugtyo2q-uc.a.run.app" \
    --http-method=GET
```



### Author
Kabilan Subramanian

### License
This project is for portfolio purposes only.



import functions_framework
from google.cloud import bigquery
import pandas as pd
import requests
from datetime import datetime
import logging
from io import BytesIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@functions_framework.http
def load_sme_data(request):  # ← This name matches --entry-point
    """Load all Excel files from the UAE SME dataset to BigQuery"""
    
    start_time = datetime.now()
    logger.info("Starting to load all SME data files")
    
    # Define all files to load
    files = {
        "sme_profiles": "https://github.com/sandrarajp/UAE-SME-Growth-Analysis-Python-SQL-PowerBI/raw/main/data/sme_profiles.xlsx",
        "monthly_kpis": "https://github.com/sandrarajp/UAE-SME-Growth-Analysis-Python-SQL-PowerBI/raw/main/data/monthly_kpis.xlsx",
        "macro_indicators": "https://github.com/sandrarajp/UAE-SME-Growth-Analysis-Python-SQL-PowerBI/raw/main/data/macro_indicators_uae_monthly.xlsx",
        "policy_events": "https://github.com/sandrarajp/UAE-SME-Growth-Analysis-Python-SQL-PowerBI/raw/main/data/policy_events.xlsx",
        "kpi_mapping": "https://github.com/sandrarajp/UAE-SME-Growth-Analysis-Python-SQL-PowerBI/raw/main/data/kpi_mapping_vision_2030.xlsx"
    }
    
    results = {}
    client = bigquery.Client()
    
    for table_name, file_url in files.items():
        try:
            logger.info(f"Processing: {table_name}")
            
            # Download and read Excel
            response = requests.get(file_url)
            response.raise_for_status()
            
            excel_data = BytesIO(response.content)
            df = pd.read_excel(excel_data, engine='openpyxl')
            
            # Clean column names (remove spaces, special chars)
            df.columns = df.columns.str.replace(' ', '_').str.lower()
            
            # Load to BigQuery
            full_table_id = f"uae-sme-analytics-pipeline.raw_zone.{table_name}"
            
            job_config = bigquery.LoadJobConfig(
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                autodetect=True
            )
            
            load_job = client.load_table_from_dataframe(df, full_table_id, job_config=job_config)
            load_job.result()
            
            results[table_name] = f"✅ Loaded {len(df)} rows"
            logger.info(f"Loaded {table_name}: {len(df)} rows")
            
        except Exception as e:
            results[table_name] = f"❌ Failed: {str(e)[:100]}"
            logger.error(f"Failed to load {table_name}: {e}")
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Build response summary
    summary = f"SUCCESS: Completed in {duration:.2f}s\n"
    for table, result in results.items():
        summary += f"\n{table}: {result}"
    
    return summary, 200
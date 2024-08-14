from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

output_file_name = datetime.now().strftime("%Y%m%d")

start_date = days_ago(1)
schedule_interval = '@daily'

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1
}

with DAG(
    dag_id="elt-reddit-pipeline",
    schedule_interval=schedule_interval,
    description="Reddit ELT Data",
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1,
    tags=["Reddit ELT"]
) as dag:
    
    extract_reddit_data = BashOperator(
        task_id="extract_reddit_data",
        bash_command=f"python /opt/airflow/extraction/extract_data_from_reddit.py {output_file_name}",
        dag=dag
    )
    extract_reddit_data.doc_md = "Extract Reddit Data and store it in a CSV file"
    
    load_to_s3 = BashOperator(
        task_id="load_to_s3",
        bash_command=f"python /opt/airflow/extraction/load_to_s3.py {output_file_name}",
        dag=dag
    )
    load_to_s3.doc_md = "Load CSV data into AWS S3 Bucket"
    
    copy_to_redshift = BashOperator(
        task_id="copy_to_redshift",
        bash_command=f"python /opt/airflow/extraction/copy_to_redshift.py {output_file_name}",
        dag=dag
    )
    copy_to_redshift.doc_md = "Copy S3 CSV file to Redshift table"
    
extract_reddit_data >> load_to_s3 >> copy_to_redshift

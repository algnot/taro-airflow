from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from model.logger import Logger
from model.common import get_next_datetime_schedule_by_schedule

schedule="5 0 * * * *"

with DAG(dag_id="update_notion_status_job", 
         description="Sync Notion Status Job", 
         start_date=get_next_datetime_schedule_by_schedule(schedule),
         tags=["notion"],  
         schedule=schedule) as dag:
    
    logger = Logger()

    @task()
    def notify_start_job():
        logger.notify("🐶 Start Update Notion Status Job")
        
    @task()
    def update_notion_status_job():
        logger.notify("End Update Notion Status Job")

    notify_start_job() >> update_notion_status_job()
    
    
    
from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from model.logger import Logger
from time import tzset
from requests import get

tzset()


with DAG(dag_id="daily_login",
         description="Daily login",
         start_date=datetime.now() - timedelta(days=1),
         schedule_interval="0 22 * * *",
         tags=["pokemon"]) as dag:
    
    logger = Logger()
    
    @task()
    def add_user_to_database():
        get("http://discord-bot:5000/caller?function=daily-check")
        logger.info("Alert Daily Login to Discord successfully :)")

    add_user_to_database()
    
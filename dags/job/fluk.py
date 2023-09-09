from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from model.logger import Logger
import time

time.tzset()

schedule = "5 0 * * * *"

with DAG(dag_id="fluckkk",
         description="Fluckkk",
         start_date=datetime.now(),
         tags=["fluck"],
         schedule=schedule) as dag:

    logger = Logger()

    @task()
    def fluk():
        logger.error("🐶 ฟลุ๊คเป็นคนกด")
            
    fluk() 

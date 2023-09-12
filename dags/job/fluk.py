from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from model.logger import Logger
from time import tzset

tzset()

schedule = "0 0 * * *"

with DAG(dag_id="fluckkk",
         description="Fluckkk",
         start_date=datetime.now() - timedelta(days=1),
         tags=["fluck"],
         schedule_interval=schedule) as dag:

    logger = Logger()

    @task()
    def fluk():
        logger.error("🐶 ฟลุ๊คเป็นคนกด")
            
    fluk() 

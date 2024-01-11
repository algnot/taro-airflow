from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from model.config import Config
from time import tzset
from common.handle_error import handle_error
from model.logger import Logger
from requests import get

tzset()


with DAG(dag_id="change_all_user_name",
         description="Change all user name",
         start_date=datetime.now() - timedelta(days=1),
         schedule="@once",
         tags=["discord"]) as dag:
    
    config = Config()
    logger = Logger()
    
    @task()
    @handle_error
    def change_all_user_name(*args, **kwargs):
        get("http://discord-bot:5000/caller?function=change-all-user-name")
    
    change_all_user_name()
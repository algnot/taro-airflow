from requests import get, post

from airflow import DAG
from airflow.decorators import task
from model.logger import Logger
from model.config import Config
from time import tzset

tzset()

schedule = "0 0 * * *"

with DAG(dag_id="bank",
         description="Bank",
         start_date=datetime.now(),
         tags=["Bank"],
         schedule=schedule) as dag:

    logger = Logger()
    config = Config()

    @task()
    def bank():
        random_image_url = get("https://source.unsplash.com/random").url
        
        post(url=config.get("DISCORD_USICK_ALERT_WEBHOOK_URL") , json={
            "embeds": [
                {
                    "title": "Bank รัก Tongla",
                    "description": "🔥🔥🔥🔥🔥🔥",
                    "color": 15105570,
                    "image": {
                        "url": random_image_url
                    }
                },
                ],
            })
            
    bank() 

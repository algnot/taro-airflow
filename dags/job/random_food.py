from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from model.config import Config
from model.discord import Discord
from pandas import read_csv
from numpy import random
from requests import get
from numpy import random

schedule = "0 9,12,17 * * *"

with DAG(dag_id="random_food_job",
         description="Random Food Job",
         start_date=datetime.now() - timedelta(days=1),
         tags=["discord"],         
         schedule_interval=schedule) as dag:

    config = Config()
    discord = Discord(config.get("DISCORD_RANDOM_FOOD_JOB_WEBHOOK_URL"))

    @task()
    def random_food():
        food_df = read_csv("/opt/airflow/data/food.csv", header=None, names=["food"])
        result = food_df.sample(1, random_state=random.default_rng()).iloc[0]["food"]
        now = datetime.now()
        
        image = get_image_from_text(result)
        image_url = ""
        
        if "images_results" in image and isinstance(image["images_results"], list):
            if len(image["images_results"]) > 0:
                image_url = random.choice(image["images_results"])
                if "original" in image_url:
                    image_url = image_url["original"]
        
        if 0 < now.hour < 10:
            discord.send_message(f"🍔 เช้าแล้วอย่าลืมกินข้าวนะ! คุณควรกินข้าวกับ **{result}**", image_url)
        elif 10 < now.hour < 15:
            discord.send_message(f"🍔 เที่ยงแล้วอย่าลืมกินข้าวนะ! คุณควรกินข้าวกับ **{result}**", image_url)
        else:
            discord.send_message(f"🍔 เย็นแล้วอย่าลืมกินข้าวนะ! คุณควรกินข้าวกับ **{result}**", image_url)
            
    def get_image_from_text(text):
        base_url = config.get("SERPAPT_BASE_URL")
        api_key = config.get("SERPAPT_API_SECRET")
        response = get(f"{base_url}/search?q={text}&tbm=isch&ijn=0&api_key={api_key}")
        return response.json()
            
    random_food() 

from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from model.config import Config
from model.discord import Discord
from pandas import read_csv
from numpy import random

schedule = "0 9,12,17 * * *"

with DAG(dag_id="random_food_job",
         description="Random Food Job",
         start_date=datetime.now() - timedelta(days=1),
         tags=["food", "discord"],         
         schedule_interval=schedule) as dag:

    config = Config()
    discord = Discord(config.get("DISCORD_RANDOM_FOOD_JOB_WEBHOOK_URL"))

    @task()
    def random_food():
        food_df = read_csv("/opt/airflow/data/food.csv", header=None, names=["food"])
        result = food_df.sample(1, random_state=random.default_rng()).iloc[0]["food"]
        now = datetime.now()
        
        if 0 > now.hour > 10:
            discord.send_message(f"🍔 เช้าแล้วอย่าลืมกินข้าวนะ! คุณควรกินข้าวกับ **{result}**")
        elif 10 > now.hour > 15:
            discord.send_message(f"🍔 เที่ยงแล้วอย่าลืมกินข้าวนะ! คุณควรกินข้าวกับ **{result}**")
        else:
            discord.send_message(f"🍔 เย็นแล้วอย่าลืมกินข้าวนะ! คุณควรกินข้าวกับ **{result}**")
            
    random_food() 

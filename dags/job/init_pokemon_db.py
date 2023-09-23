from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from model.config import Config
from time import tzset
from pandas import read_csv
from sqlalchemy import create_engine
from requests import get, post
from numpy import random

tzset()


with DAG(dag_id="init_pokemon_db",
         description="Initial pokemon table",
         start_date=datetime.now() - timedelta(days=1),
         schedule="@once",
         tags=["pokemon", "discord"]) as dag:
    
    config = Config()

    @task()
    def init_pokemon_db():
        engine = create_engine(config.get("POSTGRES_URL"))
        engine.execute("DROP TABLE IF EXISTS pokemon_table")
        pokemon_df = read_csv("/opt/airflow/data/pokemon.csv")
        pokemon_df["evo_to_id"] = -1
        pokemon_df = pokemon_df.astype({
            "id": "int64",
            "name": "string",
            "evo_to_id": "int64",
            "image": "string",
            "weight": "float64",
            "height": "float64",
            "type": "string"
        })
        pokemon_df["evo_from_id"] = pokemon_df["evo_from_id"].fillna(-1)
        pokemon_df["evo_from_id"] = pokemon_df["evo_from_id"].astype("int64")
        for index, row in pokemon_df.iterrows():
            if row["evo_from_id"] != -1:
                pokemon_df.at[row["evo_from_id"], "evo_to_id"] = row["id"]
                
        pokemon_df.to_sql("pokemon_table", engine, index=False)
        
        random_pokemon = pokemon_df.sample(1, random_state=random.default_rng()).iloc[0]
        
        post(url=config.get("DISCORD_USICK_ALERT_WEBHOOK_URL") , json={
            "embeds": [
                {
                    "title": "Pokemon DB Initialized",
                    "description": "Pokemon DB Initialized Successfully\nRandom Pokemon: `" + random_pokemon["name"] + "`\n",
                    "color": 0x00ff00,
                    "image": {
                        "url": random_pokemon["image"]
                    }
                },
                ],
            })
        
        engine.dispose()
            
    init_pokemon_db() 

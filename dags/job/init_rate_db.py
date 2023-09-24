from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from model.config import Config
from time import tzset
from sqlalchemy import create_engine
from requests import get
from pandas import read_csv, DataFrame

tzset()


with DAG(dag_id="init_rate_items_db",
         description="Initial rate of items to database",
         start_date=datetime.now() - timedelta(days=1),
         schedule="@once",
         tags=["pokemon", "discord"]) as dag:
    
    config = Config()
    
    @task()
    def add_daily_rate_db():
        engine = create_engine(config.get("POSTGRES_URL"))
        engine.execute("DROP TABLE IF EXISTS daily_rate_table")
        rate_df = read_csv("/opt/airflow/data/daily_items_rate.csv")
        
        rate_df = rate_df.astype({
            "item_key": "string",
            "item_name": "string",
            "item_table": "string",
            "add_type": "string",
            "amount": "int64",
            "rate": "float64",
            "active": "bool"
        })
        
        rate_df.to_sql("daily_rate_table", engine, index=False)
    
    @task()
    def add_item_abilities_rate_db():
        engine = create_engine(config.get("POSTGRES_URL"))
        engine.execute("DROP TABLE IF EXISTS item_abilities_rate_table")
        item_df = read_csv("/opt/airflow/data/items_abilities.csv")
        
        item_df = item_df.astype({
            "item_key": "string",
            "type": "string",
            "increse_table": "string",
            "increse_key": "string",
            "min_value": "float64",
            "max_value": "float64",
            "chance": "float64"
        })
        
        print(item_df)        
        item_df.to_sql("item_abilities_rate_table", engine, index=False)
        
    @task()
    def add_level_step_of_pokemon():
        engine = create_engine(config.get("POSTGRES_URL"))
        engine.execute("DROP TABLE IF EXISTS level_step_pokemon_table")
        d = {
            "level": [], 
            "step_to_next_level": [],
            "evo_step": []
        }
        
        start_exp = 100
        for i in range(1501):
            d["level"].append(i)
            d["step_to_next_level"].append(start_exp)
            start_exp += 50
            start_exp = int(start_exp) 
            if i // 50 < 3:
                d["evo_step"].append(i // 50)
            else:
                d["evo_step"].append(3)
            
        df = DataFrame(d)
        df.to_sql("level_step_pokemon_table", engine, index=False)
                
    add_daily_rate_db()
    add_item_abilities_rate_db()
    add_level_step_of_pokemon()

from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from model.config import Config
from time import tzset
from sqlalchemy import create_engine
from requests import get
from pandas import read_csv

tzset()


with DAG(dag_id="init_daily_rate_items_to_database",
         description="Initial daily rate items to database",
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
    
    add_daily_rate_db()

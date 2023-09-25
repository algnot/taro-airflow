from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task
from model.config import Config
from time import tzset
from sqlalchemy import create_engine
from requests import get
from pandas import read_csv, DataFrame

tzset()


with DAG(dag_id="migrate_pokemon_to_db",
         description="Migrate pokemon to database",
         start_date=datetime.now() - timedelta(days=1),
         schedule="@once",
         tags=["migrate"]) as dag:
    
    config = Config()
    
    @task()
    def migrate_unactive_pokemon_exp_table():
        engine = create_engine(config.get("POSTGRES_URL"))
        engine.execute("""
            UPDATE pokemon_exp_table
            SET atk = 0,
                def = 0,
                hp = 0
            WHERE active = FALSE;
        """)
        
    migrate_unactive_pokemon_exp_table_complete = BashOperator(
        task_id="migrate_unactive_pokemon_exp_table_complete",
        bash_command="echo 'migrate_unactive_pokemon_exp_table_complete'"
    )   
    
    @task()
    def migarte_active_pokemon_exp_table():
        engine = create_engine(config.get("POSTGRES_URL"))
        engine.execute("""
            UPDATE pokemon_exp_table
            SET atk = (FLOOR(RANDOM()*(20-30+1))+30) + (FLOOR(RANDOM()*(10-20+1))+20) * level,
                def = (FLOOR(RANDOM()*(20-30+1))+30) + (FLOOR(RANDOM()*(10-20+1))+20) * level,
                hp = (FLOOR(RANDOM()*(200-300+1))+300) + (FLOOR(RANDOM()*(100-200+1))+200) * level
            WHERE active = TRUE;
        """)
        
    migrate_unactive_pokemon_exp_table() >> migrate_unactive_pokemon_exp_table_complete >> migarte_active_pokemon_exp_table()

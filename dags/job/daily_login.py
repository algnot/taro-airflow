from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from model.config import Config
from model.logger import Logger
from time import tzset
from sqlalchemy import create_engine
from requests import get
from pandas import DataFrame
from common.handle_error import handle_error

tzset()


with DAG(dag_id="sync_user_to_database_daily",
         description="Sync user to database daily",
         start_date=datetime.now() - timedelta(days=1),
         schedule_interval="0 22 * * *",
         tags=["pokemon", "discord"]) as dag:
    
    config = Config()
    logger = Logger()
    engine = create_engine(config.get("POSTGRES_URL"))
    
    @task()
    @handle_error
    def create_table(*args, **kwargs):
        engine.execute("""
            CREATE TABLE IF NOT EXISTS users_table (
                id SERIAL PRIMARY KEY,
                user_id BIGINT UNIQUE NOT NULL,
                name TEXT,
                display_name TEXT,
                display_avatar TEXT,
                created_at TIMESTAMP,
                joined_at TIMESTAMP,
                is_bot BOOLEAN,
                pokemon_id BIGINT,
                is_daily_login BOOLEAN default false
            );
            CREATE TABLE IF NOT EXISTS user_inventory_table (
                user_id BIGINT PRIMARY KEY,
                coin BIGINT default 500,
                pokeball BIGINT default 5,
                fresh_water BIGINT default 3,
                banana BIGINT default 3,
                gem BIGINT default 2
            );
            CREATE TABLE IF NOT EXISTS pokemon_exp_table (
                user_id BIGINT,
                pokemon_id BIGINT,
                exp INTEGER,
                level INTEGER,
                active BOOLEAN default true,
                weight FLOAT,
                height FLOAT,
                atk INTEGER,
                def INTEGER,
                hp INTEGER,
                evo_step BIGINT default 0,
                critical_rate DOUBLE default 0,
                critical_damage DOUBLE default 0,
                real_damage DOUBLE default 0
            );
            CREATE TABLE IF NOT EXISTS vote_table (
                id BIGINT PRIMARY KEY,
                topic TEXT,
                description TEXT,
                create_by BIGINT
            );
            CREATE TABLE IF NOT EXISTS choice_table (
                id SERIAL PRIMARY KEY,
                vote_id BIGINT REFERENCES vote_table(id),
                index BIGINT,
                name TEXT,
                count BIGINT default 0
            );
            CREATE TABLE IF NOT EXISTS vote_user_table (
                id SERIAL PRIMARY KEY,
                vote_id BIGINT REFERENCES vote_table(id),
                choice_id BIGINT REFERENCES choice_table(id),
                user_id BIGINT 
            );
        """)
        
    create_table_complete = BashOperator(
        task_id="create_table_complete",
        bash_command="echo 'Create table complete'"
    )   
    
    @task()
    @handle_error
    def add_user_to_database(*args, **kwargs):
        users = get("http://discord-bot:5000/caller?function=get-user").json()["datas"]
        for user in users:
            engine.execute("""
                INSERT INTO users_table (user_id, name, display_name, display_avatar, created_at, joined_at, is_bot)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    display_name = EXCLUDED.display_name,
                    display_avatar = EXCLUDED.display_avatar,
                    is_daily_login = FALSE
            """, (
                user["user_id"],
                user["name"],
                user["display_name"],
                user["display_avatar"],
                user["created_at"],
                user["joined_at"],
                user["is_bot"]
            ))
            engine.execute("""
                INSERT INTO user_inventory_table (user_id)
                VALUES (%s)
                ON CONFLICT (user_id) DO NOTHING
            """, (user["user_id"]))
        engine.dispose()
        
    add_user_to_database_complete = BashOperator(
        task_id="add_user_to_database_complete",
        bash_command="echo 'Add user to database complete'"
    )
    
    @task()
    @handle_error
    def send_daily_login(*args, **kwargs):
        get("http://discord-bot:5000/caller?function=daily-check")
    
    create_table() >> create_table_complete >> add_user_to_database() >> add_user_to_database_complete >> send_daily_login()

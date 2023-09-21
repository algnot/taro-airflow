from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from model.config import Config
from model.logger import Logger
from time import tzset
from sqlalchemy import create_engine
from requests import get
from pandas import DataFrame

tzset()


with DAG(dag_id="add_user_to_database",
         description="Add user to database",
         start_date=datetime.now() - timedelta(days=1),
         schedule_interval="0 22 * * *",
         tags=["pokemon"]) as dag:
    
    config = Config()
    logger = Logger()
    engine = create_engine(config.get("POSTGRES_URL"))
    
    @task()
    def create_table():
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
                pokemon_id BIGINT 
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
                active BOOLEAN default true
            );
        """)
    
    @task()
    def add_user_to_database():
        users = get("http://discord-bot:5000/caller?function=get-user").json()["datas"]
        for user in users:
            engine.execute("""
                INSERT INTO users_table (user_id, name, display_name, display_avatar, created_at, joined_at, is_bot)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    display_name = EXCLUDED.display_name,
                    display_avatar = EXCLUDED.display_avatar
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
        logger.warning("Update user to database successfully")
        engine.dispose()
        
    def main():
        create_table()
        add_user_to_database()
    
    main()
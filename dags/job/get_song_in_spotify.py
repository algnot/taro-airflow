from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import task
from time import tzset
from model.spotify import Spotify
from random import randint
from model.discord import Discord
from model.config import Config

tzset()


with DAG(dag_id="get_song_in_spotify",
         description="Get song in spotify",
         start_date=datetime.now() - timedelta(days=1),
         schedule="@once",
         tags=["spotify", "discord"]) as dag:
    
    @task()
    def get_song_in_spotify():
        config = Config()
        spotify = Spotify()
        discord = Discord(config.get("DISCORD_SEND_SONG_WEBHOOK_URL"))
        total_song = spotify.get_count_song_in_playlist()
        random_index = randint(0, total_song - 1)
        
        song = spotify.get_song_in_playlist_by_index(random_index)
        discord.send_message(song["external_urls"]["spotify"])
    
    get_song_in_spotify()
    

import discord
from common.spotify import Spotify
from random import randint

async def on_request_music_message(message: discord.Message, is_admin: bool):
    if not is_admin:
        await message.add_reaction("❌")
        return
    
    spotify = Spotify()
    total_song = spotify.get_count_song_in_playlist()
    random_index = randint(0, total_song - 1)
    song = spotify.get_song_in_playlist_by_index(random_index)
    
    await message.channel.send(song["external_urls"]["spotify"])
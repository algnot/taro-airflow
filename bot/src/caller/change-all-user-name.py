import discord
from config import Config
from datetime import datetime
import asyncio
from pandas import read_csv
from numpy import random

def handle(bot : discord.Client):
    asyncio.run_coroutine_threadsafe(change_all_username(bot), bot.loop)
    
    return { 
        "status": "Job is running!"
    }

async def change_all_username(bot : discord.Client):
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    # food_df = read_csv("/src/data/food.csv", header=None, names=["food"])
    
    guilds = bot.guilds
    for guild in guilds:
        if guild.id != discord_guild_id:
            continue
        members = guild.members
        index = 1
        change_name_config = config.get("DISCORD_CHANGE_NAME_CONFIG", " ")
        for member in members:
            if member.bot:
                continue
            change_name_config = change_name_config.replace("{index}", str(index))
            asyncio.run_coroutine_threadsafe(member.edit(change_name=change_name_config), bot.loop)
    
            index += 1
            
            # result = food_df.sample(1, random_state=random.default_rng()).iloc[0]["food"]
            # asyncio.run_coroutine_threadsafe(member.edit(nick=str(result)), bot.loop)
            # dm = await member.create_dm()
            # await dm.send(f"Change your name in `u sick achoo` server to `{result}`!")
    
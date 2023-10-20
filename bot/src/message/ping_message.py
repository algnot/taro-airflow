import discord
from config import Config

async def on_ping_message(message: discord.Message, is_admin: bool):
    if not is_admin:
        return
    
    config = Config()
    
    env = config.get("ENV")
    await message.channel.send(f"pong! in `{env}` environment.")    
    
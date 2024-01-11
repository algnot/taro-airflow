import discord
from config import Config
from .ping_message import on_ping_message
from .spotify_message import on_request_music_message
from .config_message import on_get_config_message, on_set_config_message
from requests import get

async def handle_message(message: discord.Message):
    config = Config()
    if message.author.bot:
        return
    
    user = message.author
    
    admin_list = str(config.get("TARO_DISCORD_ADMIN", "")).split(",")
    is_admin = str(user.id) in admin_list
    
    content = message.content.lower()
    content_splited = message.content.split(" ")
    
    if is_admin:
        await message.add_reaction("🐶")
    
    if content == "ping":
        await on_ping_message(message, is_admin)
        
    elif "ทาโร่" in message.content and "เพลง" in message.content:
        await on_request_music_message(message, is_admin)
        
    elif content_splited[0].lower() == "config" and  content_splited[1].lower() == "get":
        await on_get_config_message(message, content_splited[2], is_admin)
        
    elif content_splited[0].lower() == "config" and  content_splited[1].lower() == "set":
        await on_set_config_message(message, content_splited[2], content_splited[3], is_admin)
    
    elif content == "deploy ดีไหม":
        response = get("https://deploydeemai.today/api")
        result = response.json()
        await message.channel.send(f"{'✅' if result['deploydeemai'] else '❌'} {result['message']}")
        
        
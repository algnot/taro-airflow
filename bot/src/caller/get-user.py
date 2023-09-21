import discord
from config import Config
from datetime import datetime

def handle(bot : discord.Client):
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    results = []
    
    guilds = bot.guilds
    for guild in guilds:
        if guild.id != discord_guild_id:
            continue
        members = guild.members
        for member in members:
            result = {}
            result["user_id"] = member.id
            result["name"] = member.name
            result["display_name"] = member.display_name
            result["display_avatar"] = str(member.display_avatar)
            result["created_at"] = member.created_at.strftime("%Y-%m-%d %H:%M:%S")
            result["joined_at"] = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
            result["is_bot"] = member.bot
            results.append(result)
        
    return {
        "datas": results
    }
        

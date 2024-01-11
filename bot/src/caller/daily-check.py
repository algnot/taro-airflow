import discord
from config import Config
from datetime import datetime
import asyncio
from database.user import User

def handle(bot : discord.Client):
    asyncio.run_coroutine_threadsafe(daily_check(bot), bot.loop)

async def daily_check(bot : discord.Client):
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    discord_channel_id = int(config.get("DISCORD_CHANNEL_PLAY_WITH_TARO"))
    
    guild = bot.get_guild(discord_guild_id)
    channel = guild.get_channel(discord_channel_id)
    
    today = datetime.now()
    tomorrow = today.replace(day=today.day+1, hour=0, minute=0, second=0, microsecond=0)
    tomorrow = tomorrow.strftime("%d/%m/%Y")
    
    embed = discord.Embed(title=f"✨ 🔥 ของรางวัลประจำวันที่ {tomorrow}", description="รีเซ็ททุก 22:00 ใช้คำสั่ง `/daily` เพื่อรับของรางวัล", color=0x00ff00)
    
    await channel.send(embed=embed, delete_after=60*60*24)

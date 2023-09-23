import discord
from config import Config
from logger import Logger
from datetime import datetime
import asyncio
from datetime import datetime
from database.user import User

def handle(bot : discord.Client):
    asyncio.run_coroutine_threadsafe(daily_check(bot), bot.loop)

async def daily_check(bot : discord.Client):
    config = Config()
    logger = Logger()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    discord_channel_id = int(config.get("DISCORD_CHANNEL_PLAY_WITH_TARO"))
    
    guild = bot.get_guild(discord_guild_id)
    channel = guild.get_channel(discord_channel_id)
    
    today = datetime.now()
    tomorrow = today.replace(day=today.day+1, hour=0, minute=0, second=0, microsecond=0)
    tomorrow = tomorrow.strftime("%d/%m/%Y")
    
    embed = discord.Embed(title=f"✨ 🔥 ของรางวัลประจำวันที่ {tomorrow}", description="รีเซ็ททุก 22:00 กดปุ่มด้านล่างเพื่อรับของรางวัล (1 ครั้ง/วัน/คน)", color=0x00ff00)
    daily_btn = discord.ui.Button(label="🔥 รับของรางวัลเลย", style=discord.ButtonStyle.green, custom_id="daily_login_btn")
    view = discord.ui.View()
    view.add_item(daily_btn)
    
    async def on_button_click(interaction):
        try:
          user = User(interaction.user.id)
          user_info = user.user_info
          
          if user_info["is_daily_login"]:
            await interaction.channel.send(f"❌ {interaction.user.mention} ได้รับของรางวัลไปแล้ว ไม่สามารถรับซ้ำได้")
            return
        
          item_info = user.update_daily_login()
          await interaction.channel.send(f"✨ {interaction.user.mention} ได้รับ `{item_info['item_name']}` จำนวน {item_info['amount']}")

        except Exception as e:
          logger.error(f"[Discord Login Daily] get error {str(e)}")
          await interaction.channel.send(f"❌ {interaction.user.mention} ไม่สามารถรับของรางวัลได้ กรุณาลองใหม่อีกครั้งในภายหลัง")
          raise e

    daily_btn.callback = on_button_click
    
    await channel.send(embed=embed, delete_after=60*60*24, view=view)

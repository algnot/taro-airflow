import discord
from config import Config
from logger import Logger
from database.user import User


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "daily"
    description = "รับของรางวัลประจำวัน"
    
    config = Config()
    logger = Logger()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        
        message = await interaction.followup.send("⌛ กำลังเตรียมของรางวัล...")
        
        try:
          user = User(interaction.user.id)
          user_info = user.user_info
          
          if user_info["is_daily_login"]:
            await message.edit(content=f"❌ {interaction.user.mention} ได้รับของรางวัลไปแล้ว ไม่สามารถรับซ้ำได้")
            return
        
          discord_channel_id = int(config.get("DISCORD_CHANNEL_PLAY_WITH_TARO"))
          channel = interaction.guild.get_channel(discord_channel_id)
        
          item_info = user.update_daily_login()
          
          message = await message.edit(content=f"ได้รับ `{item_info['item_name']}` จำนวน {item_info['amount']}")
          await channel.send(f"✨ {interaction.user.mention} ได้รับ `{item_info['item_name']}` จำนวน {item_info['amount']}")
          
        except Exception as e:
          logger.error(f"[Discord Login Daily] get error {str(e)}")
          await message.edit(content="❌ ไม่สามารถรับของรางวัลได้ กรุณาลองใหม่อีกครั้งในภายหลัง")
          await interaction.channel.send(f"❌ {interaction.user.mention} ไม่สามารถรับของรางวัลได้ กรุณาลองใหม่อีกครั้งในภายหลัง")
          raise e
        
        
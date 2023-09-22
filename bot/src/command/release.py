import discord
from config import Config
from logger import Logger
from database.user import User
from database.pokemon import Pokemon


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "release"
    description = "ปล่อยโปเกม่อนของคุณ"
    
    config = Config()
    logger = Logger()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        
        user = User(interaction.user.id)
        user_pokemon = user.get_user_pokemon()
        
        if not user_pokemon:
            return await interaction.followup.send("❌ คุณไม่มีโปเกม่อน ไม่สามารถปล่อยโปเกม่อนได้ `/help` เพื่อดูคำสั่งเพิ่มเติม")
        
        message = await interaction.followup.send("⌛ กำลังปล่อยโปเกม่อน...")
        
        try:
          await message.edit(content="✅ ปล่อยโปเกม่อนสำเร็จแล้ว!")
          pokemon = Pokemon()
          pokemon_info = pokemon.get_pokemon_by_id(user_pokemon["pokemon_id"])
          
          user.action_release_pokemon()
          embed = discord.Embed(title="😢 ลาก่อนนะคู่หู",
                                description=f"**{user.user_info['name']}** ได้ปล่อย **{pokemon_info['name']}** \n",
                                color=0xff0000)
          embed.set_image(url=pokemon_info["image"])
          await message.edit(embed=embed)
          
        except Exception as e:
          logger.error(str(e))
          await message.edit(content="❌ ไม่สามารถปล่อยโปเกม่อนได้ โปรดลองใหม่อีกครั้ง")
        
        
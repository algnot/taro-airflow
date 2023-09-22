import discord
from config import Config
from database.user import User


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "help"
    description = "ดูคำสั่งทั้งหมด"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        
        await interaction.followup.send("📜 คำสั่งทั้งหมด\n"
                                        "`/random` สุ่มโปเกม่อน (ใช้ Pokéball 1 ลูก)\n"
                                        "`/partner` ดูโปเกม่อนของคุณ\n"
                                        "`/release` ปล่อยโปเกม่อนของคุณ\n"
                                        "`/me` ดูข้อมูลของคุณ")
        
        
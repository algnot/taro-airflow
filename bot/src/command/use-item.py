import discord
from config import Config
from database.user import User
from database.pokemon import Pokemon
import enum


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "use-item"
    description = "ใช้ไอเทม"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    class Items(enum.Enum):
        FreshWater = "fresh_water"
        Banana = "banana"
        Gem = "gem"
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    @discord.app_commands.describe(item="ไอเทมที่ต้องการใช้", amount="จำนวนที่ต้องการใช้")
    async def call(interaction: discord.Interaction, item: Items, amount: int = 1):
        await interaction.response.defer(thinking=True, ephemeral=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        
        if amount < 1:
            return await interaction.followup.send("❌ จำนวนที่ต้องการใช้ต้องมากกว่า 0")
        
        await interaction.followup.send("command not implemented yet")
        
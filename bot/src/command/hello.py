import discord
from config import Config


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "hello"
    description = "ทักทายแบบชาวร็อค"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.send_message("เป็นควยไร")
     
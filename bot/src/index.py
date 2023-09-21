from config import Config
import discord
import os

config = Config()
bot = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(bot)

for file in os.listdir("/src/command"):
    if file.endswith(".py") and file != "__init__.py":
        file_name = file.split(".")[0]
        handle = getattr(__import__(f"command.{file_name}", fromlist=["handle"]), "handle")
        handle(bot, tree)

@bot.event
async def on_ready():
    guilds = bot.guilds
    for guild in guilds:
        await tree.sync(guild=discord.Object(id=guild.id))

bot.run(config.get("TARO_DISCORD_TOKEN"))
from logger import Logger
from config import Config
from database.pokemon import Pokemon
import discord

logger = Logger()
config = Config()

bot = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(bot)
discord_guild_id = int(config.get("DISCORD_GUILD_ID"))

@tree.command(name="hello", description="ทักทายแบบชาวร็อค", guild=discord.Object(id=discord_guild_id))
async def hello_command(interaction: discord.Interaction):    
    await interaction.response.send_message("เป็นควยไร")
    
@tree.command(name="random", description="สุ่ม Pokemon (ไม่ได้ซื้อ)", guild=discord.Object(id=discord_guild_id))
async def hello_command(interaction: discord.Interaction):  
    pokemon = Pokemon(config.get("POSTGRES_URL"))
    random_pokemon = pokemon.get_random_pokemon()
    embed = discord.Embed(title=f"**{random_pokemon['name']}** ฉันเลือกนาย!\n",
                          description=f"คุณสุ่มได้ **{random_pokemon['name']}** `({random_pokemon['id']})`\n"
                                      f"ประเภท: **{random_pokemon['type']}**\n",
                          color=0x00ff00)
    embed.set_image(url=random_pokemon["image"])
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    guilds = bot.guilds
    for guild in guilds:
        await tree.sync(guild=discord.Object(id=guild.id))

bot.run(config.get("TARO_DISCORD_TOKEN"))
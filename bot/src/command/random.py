import discord
from database.pokemon import Pokemon
from config import Config


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "random"
    description = "สุ่ม Pokemon (ไม่ได้ซื้อ)"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        if not bot.is_ready():
            await interaction.response.send_message("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
            return
        
        pokemon = Pokemon()
        random_pokemon = pokemon.get_random_pokemon()
        embed = discord.Embed(title=f"**{random_pokemon['name']}** ฉันเลือกนาย!\n",
                            description=f"คุณสุ่มได้ **{random_pokemon['name']}** `({random_pokemon['id']})`\n"
                                        f"ประเภท: **{random_pokemon['type']}**\n",
                            color=0x00ff00)
        embed.set_image(url=random_pokemon["image"])
        await interaction.response.send_message(embed=embed)
     
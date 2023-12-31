import discord
from config import Config
from database.user import User
from database.pokemon import Pokemon


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "partner"
    description = "ดูโปเกม่อนของคุณ"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        
        user = User(interaction.user.id)
        user_pokemon = user.get_user_pokemon()
        
        if not user_pokemon:
            return await interaction.followup.send("❌ คุณไม่มีโปเกม่อน โปรดสุ่มโปเกม่อน `/help` เพื่อดูคำสั่ง")
        
        pokemon = Pokemon()
        pokemon_info = pokemon.get_pokemon_by_id(user_pokemon["pokemon_id"])
        
        pokemon_description = f"ประเภท: **{pokemon_info['type']}**\n" \
                            f"เลเวล: **{user_pokemon['level']}** ({round(float(user_pokemon['exp']), 3)} exp)\n" \
                            f"สัดส่วน: {round(float(user_pokemon['weight']), 3)}kg, {round(float(user_pokemon['height']), 3)}m\n" \
                            f"atk: `{round(float(user_pokemon['atk']), 3)}`, def: `{round(float(user_pokemon['def']), 3)}`, hp: `{round(float(user_pokemon['hp']), 3)}`\n"
        
        if user_pokemon["evo_step"] > 0:
            pokemon_description += f"critacal rate: `{user_pokemon['critical_rate']}%`\n" \
                                   f"critacal damage: `{float(user_pokemon['critical_damage']) + 100.00}%`\n" \
                                   f"real damage: `{user_pokemon['real_damage']}%`\n"
        
        embed = discord.Embed(title=f"**{pokemon_info['name']}** คือคู่หูของ {user.user_info['name']}\n",
                              description=pokemon_description,
                              color=0x00ff00)
        
        embed.set_image(url=pokemon_info["image"])
        await interaction.followup.send(embed=embed)
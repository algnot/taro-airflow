import discord
from config import Config
from database.user import User
from database.pokemon import Pokemon


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "userinfo"
    description = "ดูข้อมูลผู้เล่น"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer(thinking=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        
        user = User(user.id)
        
        embed = discord.Embed(type="article", color=0xff8c00)
        embed.set_author(name=f"ข้อมูลของ {user.user_info['name']}\n", icon_url=user.user_info["display_avatar"])
        embed.add_field(name="🔴 ไอเท็ม\n",
                        value=f"_\nPokéball: {user.user_info['pokeball']}\n"
                              f"Coin: {user.user_info['coin']}\n"
                              f"Fresh Water: {user.user_info['fresh_water']}\n"
                              f"Banana: {user.user_info['banana']}\n"
                              f"Gem: {user.user_info['gem']}\n",
                        inline=True)
        
        user_pokemon = user.get_user_pokemon()
        
        if user_pokemon:
            pokemon = Pokemon()
            pokemon_info = pokemon.get_pokemon_by_id(user_pokemon["pokemon_id"])
            
            embed.add_field(name="🟢 คู่หู\n",
                            value=f"_\n{pokemon_info['name']}\n\n"
                                  f"ประเภท: {pokemon_info['type']}\n"
                                  f"เลเวล: {user_pokemon['level']}",
                            inline=True)
            embed.set_image(url=pokemon_info["image"])
        else:
            embed.add_field(name="🟢 คู่หู", value="_", inline=True)
                        
        await interaction.followup.send(embed=embed)
import discord
from config import Config
from database.user import User
from database.pokemon import Pokemon
from random import randint, random


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "battle"
    description = "ต่อสู้กับผู้เล่นคนอื่น"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer(thinking=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        
        player_1 = User(interaction.user.id)
        player_2 = User(user.id)
        
        player_1_pokemon = player_1.get_user_pokemon()
        player_2_pokemon = player_2.get_user_pokemon()
        
        if not player_1_pokemon:
            return await interaction.followup.send("❌ คุณไม่มีคู่หูในการต่อสู้")
        
        if not player_2_pokemon:
            return await interaction.followup.send("❌ คู่ต่อสู้ไม่มีคู่หูในการต่อสู้")
        
        message = await interaction.followup.send("⌛ กำลังต่อสู้...")
        
        round_of_game = 1
        round_of_player = randint(1, 100) % 2 + 1
        
        player_1_hp = player_1_pokemon["hp"]
        player_1_atk = player_1_pokemon["atk"]
        player_1_def = player_1_pokemon["def"]
        player_2_hp = player_2_pokemon["hp"]
        player_2_atk = player_2_pokemon["atk"]
        player_2_def = player_2_pokemon["def"]
        
        pokemon = Pokemon()
        player_1_pokemon_info = pokemon.get_pokemon_by_id(player_1_pokemon["pokemon_id"])
        player_2_pokemon_info = pokemon.get_pokemon_by_id(player_2_pokemon["pokemon_id"])
        
        summary_message = f"🔥 {player_1_pokemon_info['name']} {interaction.user.mention} ต่อสู้กับ {player_2_pokemon_info['name']} {user.mention}\n"
        
        while player_1_hp > 0 and player_2_hp > 0:                        
            # atk of attack player
            random_float = round(random() * (1.0 - 0.7) + 0.7, 2)
            attack = player_1_atk if round_of_player == 1 else player_2_atk
            attack = int(attack * random_float)
            
            # def of defense player
            random_float = round(random() * (7.0 - 0.3) + 0.3, 2)
            defense = player_2_def if round_of_player == 1 else player_1_def
            hp = player_2_hp if round_of_player == 1 else player_1_hp
            defense = int(defense * random_float)
            
            if attack > defense:
                hp = hp - (attack - defense)
            
            content = ""
                            
            if round_of_player == 1:
                if attack <= defense:
                    content = f"{round_of_game} - `{player_1_pokemon_info['name']}` โจมตี `{player_2_pokemon_info['name']}` ด้วยพลัง `{attack}` กันได้ `{attack}` ไม่เกิดความเสียหาย (เหลือ hp `{player_2_hp}`)"
                else:
                    player_2_hp = hp - (attack - defense) if hp - (attack - defense) > 0 else 0
                    content = f"{round_of_game} - `{player_1_pokemon_info['name']}` โจมตี `{player_2_pokemon_info['name']}` ด้วยพลัง `{attack}` กันได้ `{defense}` เสียหาย `{attack - defense}` (เหลือ hp `{player_2_hp}`)"
                
            if round_of_player == 2:
                if attack <= defense:
                    content = f"{round_of_game} - `{player_2_pokemon_info['name']}` โจมตี `{player_1_pokemon_info['name']}` ด้วยพลัง `{attack}` กันได้ `{attack}` ไม่เกิดความเสียหาย (เหลือ hp `{player_1_hp}`)"
                else:
                    player_1_hp = hp - (attack - defense) if hp - (attack - defense) > 0 else 0
                    content = f"{round_of_game} - `{player_2_pokemon_info['name']}` โจมตี `{player_1_pokemon_info['name']}` ด้วยพลัง `{attack}` กันได้ `{defense}` เสียหาย `{attack - defense}` (เหลือ hp `{player_1_hp}`)"
            
            summary_message += f"{content}\n"
            await message.edit(content=f"🔥 {player_1_pokemon_info['name']} {interaction.user.mention} ต่อสู้กับ {player_2_pokemon_info['name']} {user.mention}\n{content}")
            round_of_player = 1 if round_of_player == 2 else 2       
            round_of_game += 1
                
        embed = discord.Embed(type="article", color=0xff8c00)
        
        if player_1_hp <= 0:
            # player 2 win
            embed.set_author(name=f"🎉 {player_2_pokemon_info['name']} ของ {player_2.user_info['name']} เป็นฝ่ายชนะ!", icon_url=player_2.user_info["display_avatar"])
            embed.set_image(url=player_2_pokemon_info["image"])
        else:
            # player 1 win
            embed.set_author(name=f"🎉 {player_1_pokemon_info['name']} ของ {player_1.user_info['name']} เป็นฝ่ายชนะ!", icon_url=player_1.user_info["display_avatar"])
            embed.set_image(url=player_1_pokemon_info["image"])
            
        icon_player_1 = "🔴" if player_1_hp <= 0 else "🟢"
        icon_player_2 = "🔴" if player_2_hp <= 0 else "🟢"
        
        embed.add_field(name=f"{icon_player_1} {player_1.user_info['name']}", 
                        value=f"{interaction.user.mention}\n"
                              f"คู่หู `{player_1_pokemon_info['name']}`\n"
                              f"atk `{player_1_pokemon['atk']}`\n"
                              f"def `{player_1_pokemon['def']}`\n"
                              f"hp `{player_1_pokemon['hp']}`", inline=True)
        
        embed.add_field(name=f"{icon_player_2} {player_2.user_info['name']}",
                        value=f"{user.mention}\n"
                              f"คู่หู `{player_2_pokemon_info['name']}`\n"
                              f"atk `{player_2_pokemon['atk']}`\n"
                              f"def `{player_2_pokemon['def']}`\n"
                              f"hp `{player_2_pokemon['hp']}`", inline=True)
        
        embed.set_footer(text=f"จำนวนรอบการต่อสู้ `{round_of_game - 1}` รอบ")
        
        await interaction.followup.send(embed=embed)
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
    discord_channel_id = int(config.get("DISCORD_CHANNEL_PLAY_WITH_TARO"))
    
    class Items(enum.Enum):
        FreshWater = "fresh_water"
        Banana = "banana"
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    @discord.app_commands.describe(item="ไอเทมที่ต้องการใช้", amount="จำนวนที่ต้องการใช้")
    async def call(interaction: discord.Interaction, item: Items, amount: int = 1):
        await interaction.response.defer(thinking=True, ephemeral=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        
        if amount < 1:
            return await interaction.followup.send("❌ จำนวนที่ต้องการใช้ต้องมากกว่า 0")
        
        user = User(interaction.user.id)
        user_info = user.user_info
        user_pokemon = user.get_user_pokemon()
                
        if not user_pokemon:
            return await interaction.followup.send("❌ ยังไม่มีโปเกมอนไม่สามารถใช้ไอเทมได้กรุณาเพิ่มโปเกมอนก่อน โดยใช้คำสั่ง `/random`")
        
        if user_info[item.value] < amount:
            return await interaction.followup.send(f"❌ ไอเทมไม่เพียงพอ (คงเหลือ `{user_info[item.value]}` {item.name})")
        
        if amount > 10:
            return await interaction.followup.send("❌ สามารถใช้ไอเทมได้ไม่เกิน 10 ชิ้นต่อครั้ง")
        
        message = await interaction.followup.send("⌛ กำลังใช้ไอเทม...")
        
        try:
            result, is_level_up = user.use_item(item.value, amount)
            pokemon = Pokemon()
            pokemon_info = pokemon.get_pokemon_by_id(user_pokemon["pokemon_id"])
            message_result = f"✅ ใช้ {item.name} จำนวน {amount} ชิ้นแล้ว\n"
            for ability in result:
                message_result += f"✅ `{pokemon_info['name']}` ของคุณ ได้รับ `{ability['increse_key']}` จำนวน `{ability['value']}`\n"
            
            if is_level_up:
                channel = interaction.guild.get_channel(discord_channel_id)
                
                embed = discord.Embed(type="article", color=0x00ff00)
                embed.set_author(name=f"🎉 โปเกมอนของ {user_info['name']} เลเวลอัพแล้ว", 
                                 icon_url=user.user_info["display_avatar"])
                embed.add_field(name=f"{pokemon_info['name']}",
                                value=f"อัพเลเวลจาก {is_level_up['old_level']} เป็นเลเวล {is_level_up['new_level']}",
                                inline=True)
                embed.set_thumbnail(url=pokemon_info["image"])
                await channel.send(embed=embed)
                
                if is_level_up["old_evo_step"] != is_level_up["new_evo_step"]:
                    old_pokemon_name = pokemon_info["name"]
                    user_pokemon = user.get_user_pokemon()
                    pokemon_info = pokemon.get_pokemon_by_id(user_pokemon["pokemon_id"])
                    evo_embed = discord.Embed(type="article", color=0x00ff00)
                    evo_embed.set_author(name=f"🎉 {old_pokemon_name} ได้อีโวเป็น {pokemon_info['name']}", 
                                        icon_url=user.user_info["display_avatar"])
                    evo_embed.add_field(name="ความสามารถเพิ่มเติม",
                                        value=f"critacal rate: `{user_pokemon['critical_rate']}%`\n"
                                            f"cretical damage: `{user_pokemon['critical_damage'] + 100}%`\n"
                                            f"real damage: `{user_pokemon['real_damage']}%`",
                                        inline=True)   
                    evo_embed.set_thumbnail(url=pokemon_info["image"])
                    await channel.send(embed=evo_embed)
                    
            await message.edit(content=message_result)
            
        except Exception as e:
            await interaction.followup.send("❌ ไม่สามารถใช้ไอเทมได้ กรุณาลองใหม่อีกครั้ง")
            raise e
        
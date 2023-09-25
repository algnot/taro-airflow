import discord
from config import Config
from logger import Logger
from database.user import User


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "random"
    description = "สุ่มโปเกม่อน (ใช้ Pokéball 1 ลูก)"
    
    config = Config()
    logger = Logger()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
            
        user = User(interaction.user.id)
        user_info = user.user_info
        user_pokemon = user.get_user_pokemon()
                
        if user_pokemon:
            return await interaction.followup.send("❌ มีโปเกม่อนได้แค่คัวเดียว ต้องปล่อยโปเกม่อนตัวเก่าก่อน `/help` เพื่อดูคำสั่ง")
        
        if user_info["pokeball"] < 1:
            return await interaction.followup.send("❌ คุณไม่มี Pokéball ในคลัง โปรดซื้อ Pokéball `/help` เพื่อดูคำสั่ง")
        
        message = await interaction.followup.send("⌛ ใช้ 1 Pokéball ในการจับโปเกม่อน...")
        
        try:
            await message.edit(content="⌛ กำลังสุ่มโปเกม่อน...")
            random_pokemon, pokemon_abilities = user.action_get_random_pokemon()
            await message.edit(content=f"✅ สุ่มโปเกม่อนสำเร็จแล้ว! (คงเหลือ {user_info['pokeball'] - 1} Pokéball)")
            
            embed = discord.Embed(title=f"**{random_pokemon['name']}** ฉันเลือกนาย!\n",
                                description=f"**{user_info['name']}** สุ่มได้ **{random_pokemon['name']}** `({random_pokemon['id']})`\n"
                                            f"ประเภท: **{random_pokemon['type']}**\n"
                                            f"atk: `{pokemon_abilities['atk']}` def: `{pokemon_abilities['def']}`  hp: `{pokemon_abilities['hp']}`\n",
                                color=0x00ff00)
            embed.set_image(url=random_pokemon["image"])
            await message.edit(embed=embed)
            
        except Exception:
            logger.error(str(e))
            await message.edit(content="❌ ไม่สามารถสุ่มโปเกม่อนได้ โปรดลองใหม่อีกครั้ง")
        
        
     
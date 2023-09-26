import discord
from config import Config
from database.shop import Shop


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "shop-info"
    description = "ดูรายละเอียดร้านค้า"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        
        shop = Shop()
        items = shop.get_shop_items()
        
        result = ""
        count = 0
        for item in items:
            count += 1
            result += f"{count}. `{item['item_name']}` ราคา {item['buy']} coin ขายได้ {item['sell']} coin\n"
            
        if not result:
            return await interaction.followup.send("🏪 ร้านค้า\n-- ยังไม่มีสินค้าในร้านค้า --")
            
        await interaction.followup.send(f"🏪 ร้านค้า\n{result}\nซื้อสินค้าใช้คำสั่ง `/shop-buy` ขายสินค้าใช้คำสั่ง `/shop-sell`")
            
        
        
        
        
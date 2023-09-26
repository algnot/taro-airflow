import discord
from config import Config
from logger import Logger
from database.user import User
from database.shop import Shop
import enum


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "shop-buy"
    description = "ซื้อสินค้าในร้านค้า"
    
    config = Config()
    logger = Logger()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    class Items(enum.Enum):
        FreshWater = "fresh_water"
        Banana = "banana"
        Gem = "gem"
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    @discord.app_commands.describe(item="ไอเทมที่ต้องการซื้อ", amount="จำนวนที่ต้องการซื้อ")
    async def call(interaction: discord.Interaction, item: Items, amount: int = 1):
        await interaction.response.defer(thinking=True, ephemeral=True)
        if not bot.is_ready():
            return await interaction.followup.send("⌛ รอสักครู่นะครับ กำลังเปิดระบบอยู่...")
        
        shop = Shop()
        user = User(interaction.user.id)
        
        coin_of_user = user.user_info["coin"]
        item_info = shop.get_shop_item(item.value)
        
        logger.info(f"{item.value} {item_info}")
        
        if not item_info:
            return await interaction.followup.send("❌ ไม่มีสินค้านี้ในร้านค้า")
        
        if item_info[0]["buy"] * amount > coin_of_user:
            return await interaction.followup.send(f"❌ ยอดเงินของคุณไม่เพียงพอ (คงเหลือ `{coin_of_user}` coin สามารถซื้อได้ `{coin_of_user // item_info[0]['buy']}`)")
        
        shop.buy_item(user.user_id, item_info[0]["item_key"], amount, item_info[0]["buy"] * amount)
        
        await interaction.followup.send(f"✅ เพิ่ม `{item_info[0]['item_name']}` จำนวน `{amount}` แล้ว")
        
        
            
        
        
        
        
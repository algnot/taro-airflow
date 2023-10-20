import discord
from config import Config

async def on_get_config_message(message: discord.Message, name:str, is_admin: bool):
    if not is_admin:
        await message.add_reaction("❌")
        return
    
    config = Config()
    value = config.get(name)
    
    if value:
        await message.channel.send(f"get config name `{name}` value ||{value}||")
    else:
        await message.channel.send(f"config name `{name}` not found")
        
async def on_set_config_message(message: discord.Message, name:str, value:str, is_admin: bool):
    if not is_admin:
        await message.add_reaction("❌")
        return
    
    config = Config()
    config.set(name, value)
    await message.channel.send(f"set config name `{name}` to `{value}`")

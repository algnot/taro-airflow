from config import Config
from logger import Logger
from flask import Flask, request, jsonify
import discord
import os
import threading
from common.spotify import Spotify
from random import randint
import traceback

config = Config()
logger = Logger()
bot = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(bot)
app = Flask(__name__)
 
for file in os.listdir("/src/command"):
    if file.endswith(".py") and file != "__init__.py":
        file_name = file.split(".")[0]
        handle = getattr(__import__(f"command.{file_name}", fromlist=["handle"]), "handle")
        handle(bot, tree)
    
async def handle_command_error(interection, error):
    await interection.followup.send("❌ ไม่สามารถใช้คำสั่งได้ โปรดลองใหม่อีกครั้ง", ephemeral=True)
    logger.error(f"[Discord Command] Can not use command with error\n```{traceback.format_exc()}```")
        
tree.on_error = handle_command_error
            
@app.route('/', methods=['GET'])
def index():
    return "Server is running :)"
            
@app.route('/caller', methods=['GET'])
def caller():
    function_id = request.args.get('function')
    if not function_id:
        return "No function id"
    try:
        caller = getattr(__import__(f"caller.{function_id}", fromlist=["handle"]), "handle")
        return_value = caller(bot)
        if return_value:
            try:
                return jsonify(return_value)
            except Exception as e:
                return str(return_value)
        return "OK"
    except Exception as e:
        logger.error(f"[Discord Caller] Can not use function {function_id} with error\n```{traceback.format_exc()}```")
        return str(e)
    
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    user = message.author
    
    admin_list = str(config.get("TARO_DISCORD_ADMIN", "")).split(",")
    
    if str(user.id) not in admin_list:
        if "ทาโร่" in message.content and "ขอเพลง" in message.content:
            await message.add_reaction("❌")
        return
        
    await message.add_reaction("🐶")
    
    if message.content == "ping":
        env = config.get("ENV")
        await message.channel.send(f"pong! in `{env}` environment.")
    
    if "ทาโร่" in message.content and "เพลง" in message.content:
        spotify = Spotify()
        total_song = spotify.get_count_song_in_playlist()
        random_index = randint(0, total_song - 1)
        song = spotify.get_song_in_playlist_by_index(random_index)
        
        await message.channel.send(song["external_urls"]["spotify"])

@bot.event
async def on_ready():
    guilds = bot.guilds
    logger.warning(f"[Discord] Bot is ready on `{config.get('ENV', 'Production')}` environment!")
    for guild in guilds:
        await tree.sync(guild=discord.Object(id=guild.id))
        
def run_discord_bot():
    bot.run(config.get("TARO_DISCORD_TOKEN"))

if __name__ == "__main__":
    discord_thread = threading.Thread(target=run_discord_bot)
    discord_thread.start()
    app.run(host='0.0.0.0')

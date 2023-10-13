from config import Config
from logger import Logger
from flask import Flask, request, jsonify
import discord
import os
import threading

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
    logger.error(f"[Discord Command] {error}")
        
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
        logger.error(f"[Discord Caller] Can not use function {function_id} with error {str(e)}")
        return str(e)

@bot.event
async def on_ready():
    guilds = bot.guilds
    for guild in guilds:
        await tree.sync(guild=discord.Object(id=guild.id))
        
def run_discord_bot():
    bot.run(config.get("TARO_DISCORD_TOKEN"))

if __name__ == "__main__":
    discord_thread = threading.Thread(target=run_discord_bot)
    discord_thread.start()
    app.run(host='0.0.0.0')

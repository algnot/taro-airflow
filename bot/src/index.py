from config import Config
from flask import Flask, request, jsonify
import discord
import os
import threading

config = Config()
bot = discord.Client(intents=discord.Intents.all())
tree = discord.app_commands.CommandTree(bot)
app = Flask(__name__)

for file in os.listdir("/src/command"):
    if file.endswith(".py") and file != "__init__.py":
        file_name = file.split(".")[0]
        handle = getattr(__import__(f"command.{file_name}", fromlist=["handle"]), "handle")
        handle(bot, tree)
        
@app.route('/', methods=['GET'])
def index():
    return "Server is running :)"
        
@app.route('/caller', methods=['GET'])
def caller():
    try:
        function_id = request.args.get('function')
        caller = getattr(__import__(f"caller.{function_id}", fromlist=["handle"]), "handle")
        return_value = caller(bot)
        if return_value:
            try:
                return jsonify(return_value)
            except Exception as e:
                return str(return_value)
        return "OK"
    except Exception as e:
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

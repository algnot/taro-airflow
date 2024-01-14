import discord
from discord import ui
from config import Config


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "vote"
    description = "สร้าง pool โหวต"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.send_modal(VoteModal(title="Create Vote 📝"))
        
def get_choice_message(choices: list):
    message = ""
    all_count = sum([choice["count"] for choice in choices]) 
    all_count = 1 if all_count == 0 else all_count
    
    for index, choice in enumerate(choices):
        percent = round((choice["count"] / all_count) * 100, 2)
        message += f"{index + 1}. {choice['name']} - {choice['count']} vote\n"
        message += f"|{'■' * int(40 * percent // 100)}{' ' * (40 - int(40 * percent // 100))}| {percent}%\n\n"
        
    return message
        
class VoteModal(discord.ui.Modal):
    topic = ui.TextInput(label="Topic", 
                         placeholder="Enter topic here")
    description = ui.TextInput(label="Description", 
                               placeholder="Enter description here", 
                               required=False)
    choice = ui.TextInput(label="Choice", 
                          placeholder="Enter choice here (separate by comma ',')")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        message = await interaction.followup.send("⌛ Vote is creating...", ephemeral=True)
        
        embed = discord.Embed(title=f"📝 Vote: {self.topic.value}", 
                              description=self.description.value)
        
        choices = self.choice.value.split(",")
        choices_list = [{"name": choice, "count": 0} for choice in choices] 
        date = interaction.created_at.strftime("%d/%m/%Y %H:%M")
        
        embed.add_field(name="Summary", value=f"```{get_choice_message(choices_list)}```")
        embed.set_footer(text=f"Vote by {interaction.user.name} at {date}", 
                         icon_url=interaction.user.display_avatar)
        
        message = await message.edit(content="✅ Vote is created!")
        await interaction.channel.send(embed=embed,
                                       view=VoteView(message.id, 
                                                     self.topic.value, 
                                                     self.description.value, 
                                                     self.choice.value))
        
class VoteView(discord.ui.View):
    def __init__(self, id, topic, description, choices):
        super().__init__()
        self.topic = topic
        self.description = description
        self.choices = choices
        
        index = 1
        for choice in self.choices.split(","):
            self.add_item(discord.ui.Button(label=f"{index}. {choice}", 
                                            style=discord.ButtonStyle.blurple, 
                                            custom_id=f"{id}-choice-{index}-{choice}"))
            index += 1
            
        self.add_item(discord.ui.Button(label="Add Choice", style=discord.ButtonStyle.gray, custom_id=f"{id}-add"))
        self.add_item(discord.ui.Button(label="Close Vote", style=discord.ButtonStyle.red, custom_id=f"{id}-close"))
        
    async def on_timeout(self):
        await self.message.edit(view=None)
        
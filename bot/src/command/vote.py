import discord
from discord import ui
from database.vote import Vote
from database.user import User
from config import Config


def handle(bot:discord.Client, tree:discord.app_commands.CommandTree):
    name = "vote"
    description = "สร้าง pool โหวต"
    
    config = Config()
    discord_guild_id = int(config.get("DISCORD_GUILD_ID"))
    
    @tree.command(name=name, description=description, guild=discord.Object(id=discord_guild_id))
    async def call(interaction: discord.Interaction):
        await interaction.response.send_modal(VoteModal(title="Create Vote 📝"))
        
    @bot.event
    async def on_interaction(interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component:
            custom_id = interaction.data["custom_id"]
            
            if custom_id.startswith("on_vote"):
                await interaction.response.defer()
                message = await interaction.followup.send("⌛ กำลังโหวต..", ephemeral=True)
                vote_id, choice = custom_id.split("on_vote-")[1].split("-", maxsplit=1)
                vote = Vote(int(vote_id))
                vote.on_vote(interaction.user.id, choice)
                embed = VoteEmbed(vote.topic, vote.description, vote.choices, interaction, vote.create_by)
                await interaction.message.edit(embed=embed)
                await message.edit(content=f"✅ {interaction.user.mention} โหวตเรียบร้อยแล้ว!")
                
            elif custom_id.startswith("on_add_choice"):
                vote_id = custom_id.split("on_add_choice-")[1]
                await interaction.response.send_modal(AddChoiceModal(title="Add Choice 📝", message_id=interaction.message.id, vote_id=vote_id))

                
class VoteEmbed(discord.Embed):
    def __init__(self, topic, description, choices, interaction, create_by_id=False):
        super().__init__(title=f"📝 Vote: {topic}", 
                         description=description)
        
        self.add_field(name="Summary", value=f"```{self.get_choice_message(choices)}```")
        
        if create_by_id:
            try:
                create_by = interaction.guild.get_member(create_by_id)
                self.set_footer(text=f"Created by {create_by.display_name}", 
                            icon_url=create_by.display_avatar)
            except AttributeError:
                user = User(create_by_id)
                if user.user_info:
                    self.set_footer(text=f"Created by {user.user_info['name']}",
                                    icon_url=user.user_info['display_avatar'])
            
    def update(self, choices):
        self.set_field_at(0, name="Summary", value=f"```{self.get_choice_message(choices)}```")
        
    def get_choice_message(self, choices: list):
        message = ""
        all_count = sum([choice["count"] for choice in choices]) 
        all_count = 1 if all_count == 0 else all_count
        
        for index, choice in enumerate(choices):
            percent = round((choice["count"] / all_count) * 100, 2)
            message += f"{index + 1}. {choice['name']} - {choice['count']} vote\n"
            message += f"|{'■' * int(40 * percent // 100)}{' ' * (40 - int(40 * percent // 100))}| {percent}%\n\n"
            
        return message
    
class AddChoiceModal(discord.ui.Modal):
    choice = ui.TextInput(label="New Choice", 
                          placeholder="Enter choice here (separate by comma ',')")
    
    def __init__(self, title: str, message_id: int, vote_id: int):
        super().__init__(title=title)
        self.vote_id = vote_id
        self.message_id = message_id
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        interaction = await interaction.followup.send("⌛ Adding choice...", ephemeral=True)
        message = await interaction.channel.fetch_message(self.message_id)
        vote = Vote(self.vote_id)
        vote.add_choice(self.choice.value.split(","))
        
        embed = VoteEmbed(vote.topic, vote.description, vote.choices, interaction, vote.create_by)
        view = VoteView(self.vote_id, vote.topic, vote.description, vote.choices)
        
        await message.edit(embed=embed, view=view)
        await interaction.edit(content="✅ Choice is added!")
        
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
        
        choices = [{"name": choice, "count": 0} for choice in self.choice.value.split(",")]
        choices = [dict(t) for t in {tuple(d.items()) for d in choices}]
        
        embed = VoteEmbed(self.topic.value, self.description.value, choices, interaction, interaction.user.id)
        
        vote = Vote(message.id)
        vote.create(self.topic.value, self.description.value, choices, interaction.user.id)
        
        message = await message.edit(content="✅ Vote is created!")
        await interaction.channel.send(embed=embed,
                                       view=VoteView(message.id, self.topic.value, self.description.value, choices))
        
class VoteView(discord.ui.View):
    def __init__(self, id, topic, description, choices):
        super().__init__(timeout=None)
        self.topic = topic
        self.description = description
        self.choices = choices
        
        for index, choice in enumerate(choices):
            self.add_item(discord.ui.Button(label=f"{index+1}. {choice['name']}", 
                                            style=discord.ButtonStyle.blurple, 
                                            custom_id=f"on_vote-{id}-{choice['name']}",
                                            row=0))
            
        self.add_item(discord.ui.Button(label="Add Choice", style=discord.ButtonStyle.gray, custom_id=f"on_add_choice-{id}", row=1))
        self.add_item(discord.ui.Button(label="Close Vote", style=discord.ButtonStyle.red, custom_id=f"on_close_vote-{id}", row=1))
        
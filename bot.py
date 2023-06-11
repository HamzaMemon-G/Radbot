import discord
import discord.ext.commands as commands
import datetime
from dotenv import load_dotenv
import os
import random
from typing import Optional

load_dotenv()

token = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready')
    await bot.tree.sync()

@bot.event
async def on_message(msg: discord.Message):

    greetings = ['hi', 'hello', 'hey', 'yo', 'sup']
    random_greeting = random.choice(greetings)
    if msg.content.lower() in greetings:
        await msg.channel.send(f'{random_greeting} {msg.author.mention}')


@bot.event
async def on_member_join(member):
    role_id = 985448617311629362
    role = member.guild.get_role(role_id)
    if role is not None:
        await member.add_roles(role)

@bot.tree.command(name="announce", description="Announce a message to a channel")
async def announce(interaction: discord.Interaction, channel: discord.TextChannel, embed: bool, *, message: str, title: Optional[str]=None, r: Optional[int]=None, g: Optional[int]=None, b: Optional[int]=None):
    await interaction.response.defer(thinking=True)
    if embed == True:
        embed = discord.Embed(title=title, description=message, color=discord.Color.from_rgb(r, g, b))
        await channel.send(embed=embed)
        await interaction.followup.send("Announcement sent!", ephemeral=True)

@bot.tree.command(name="kick", description="Kick a user")
async def kick(interaction: discord.Interaction, user: discord.Member, *, reason: str):
    await user.kick(reason=reason)
    await interaction.channel.send(f"Kicked {user.mention} for **{reason}**")
    await interaction.response.send_message(f"Kicked {user} for **{reason}**", ephemeral=True)

@bot.tree.command(name="warn", description="Warn a user")
async def warn(interaction: discord.Interaction, user: discord.Member, *, reason: str):
    await interaction.channel.send(f"Warned {user.mention} for **{reason}**")
    await interaction.response.send_message(f"Warned {user} for **{reason}**", ephemeral=True)

bot.run(token)
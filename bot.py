import discord
import discord.ext.commands as commands
import datetime
from dotenv import load_dotenv
import os
import random
from typing import Optional
import asyncio

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
async def announce(interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role, embed: bool, *, message: str, title: Optional[str]=None, author: Optional[str]=None,r: Optional[int]=255, g: Optional[int]=119, b: Optional[int]=0):
    
    if embed == True:
        embed = discord.Embed(title=title, description=message, color=discord.Color.from_rgb(r, g, b))

        if author is None:
            embed.set_footer(text=f"announcement by {interaction.user}")
        else:
            embed.set_footer(text=f"announcement by {author}")

        await interaction.response.defer(thinking=True)
        await channel.send(embed=embed)
        await channel.send(role.mention)
    else:
        await channel.send(message)
        await channel.send(role.mention)
    await interaction.followup.send("Announced your message" , ephemeral=True)


@bot.tree.command(name="kick", description="Kick a user from the server")
async def kick(interaction: discord.Interaction, user: discord.Member, *, reason: str):
    await user.kick(reason=reason)
    await interaction.channel.send(f"Kicked {user.mention} for **{reason}**")
    await interaction.response.send_message(f"Kicked {user} for **{reason}**", ephemeral=True)

@bot.tree.command(name="warn", description="Warn a user")
async def warn(interaction: discord.Interaction, user: discord.Member, *, reason: str):
    await interaction.channel.send(f"Warned {user.mention} for **{reason}**")
    await interaction.response.send_message(f"Warned {user} for **{reason}**", ephemeral=True)

@bot.tree.command(name="poll", description="Create a poll")
async def poll(interaction: discord.Interaction, *, title: str, question: str, reaction1: str, reaction2: str, duration: int, r: Optional[int]=255, g: Optional[int]=119, b: Optional[int]=0):
    embed = discord.Embed(title=title, description=question, color=discord.Color.from_rgb(r, g, b))
    embed.set_footer(text=f"Poll created by {interaction.user}")
    message = await interaction.channel.send(embed=embed)
    await message.add_reaction(reaction1)
    await message.add_reaction(reaction2)
    await interaction.response.send_message("Poll created!", ephemeral=True)

    duration = datetime.timedelta(seconds=duration)
    await asyncio.sleep(duration.total_seconds())

    message = await interaction.channel.fetch_message(message.id)

    count1 = 0
    count2 = 0

    for reaction in message.reactions:
        if reaction.emoji == reaction1:
            count1 = reaction.count - 1  
        elif reaction.emoji == reaction2:
            count2 = reaction.count - 1

    if count1 > count2:
        winner = reaction1
    elif count2 > count1:
        winner = reaction2
    else:
        winner = "Tie"

    # Send a message with the winner
    if winner == "Tie":
        result_message = "The poll ended in a tie!"
    else:
        result_message = f"The winner is {winner} with {max(count1, count2)} votes!"

    await interaction.channel.send(result_message)

@bot.tree.command(name="whois", description="Get information about a user")
async def whois(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title=f"{user}", description=f"Information about {user.mention}", color=user.color)
    embed.add_field(name="ID", value=user.id, inline=False)
    embed.add_field(name="Joined at", value=user.joined_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
    embed.add_field(name="Created at", value=user.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
    embed.set_thumbnail(url=user.display_avatar)
    embed.set_footer(text=f"Requested by {interaction.user}")
    await interaction.response.send_message(embed=embed, ephemeral=True)

    

bot.run(token)
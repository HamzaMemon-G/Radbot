import discord
import discord.ext.commands as commands
from datetime import timedelta
from dotenv import load_dotenv
import os
import random
from typing import Optional
import asyncio

load_dotenv()

token = os.getenv('BOT_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

cogs = ["cogs.utils", "cogs.mod"]

@bot.event
async def on_ready():
    print('Bot is ready')
    
    for cog in cogs:
        await bot.load_extension(cog)
    print('Loaded all cogs')

    await bot.tree.sync()

@bot.event
async def on_message(msg: discord.Message):

    greetings = ["Hi", "Hello", "Hey", "Yo","What's sup"]
    random_greeting = random.choice(greetings)
    if msg.content.lower() in greetings:
        await msg.channel.send(f'{random_greeting} {msg.author.mention}')


bot.run(token)
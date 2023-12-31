import discord
from discord.ext import commands
from discord import app_commands
from bot import MyBot
import random

greetings = ["Hello", "Hi", "Hey", "Yo", "What's up"]



class listeners(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        content = message.content.lower()
        if content in [greeting.lower() for greeting in greetings]:
            await message.channel.send(random.choice(greetings))
        elif "ip" in content.lower():
            await message.channel.send("> **IP:** `play.radarsserver.live`")
        elif "help" in content.lower():
            await message.channel.send("> **Need help?** vist `#help` channel") 

async def setup(bot: MyBot):
    await bot.add_cog(listeners(bot))
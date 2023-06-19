import discord
from discord.ext import commands
from discord import app_commands
from bot import MyBot
import random

greetings = ["Hello", "Hi", "Hey", "Yo", "What's up"]

class Greetings(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        content = message.content.lower()
        if content in [greeting.lower() for greeting in greetings]:
            await message.channel.send(random.choice(greetings))

async def setup(bot: MyBot):
    await bot.add_cog(Greetings(bot))
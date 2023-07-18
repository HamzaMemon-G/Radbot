import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
token = os.getenv('BOT_TOKEN')

cogs = ["cogs.utils", "cogs.mod", "cogs.listners", "cogs.user", "cogs.welcome"]

class MyBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)
    
    async def setup_hook(self) -> None:
        for cog in cogs:
            await bot.load_extension(cog)
        print("Loaded all cogs")

    async def on_ready(self):
        print("Bot is ready")
        while True:
            activity = discord.Game(name="Minecraft", type=discord.ActivityType.playing)
            await bot.change_presence(activity=activity)
            await asyncio.sleep(30)
            activity = discord.Activity(name="RADAR'S SERVER", type=discord.ActivityType.watching)
            await bot.change_presence(activity=activity)
            await asyncio.sleep(30)

if __name__ == "__main__":

    bot = MyBot(command_prefix='!', intents=discord.Intents.all())
    bot.run(token)
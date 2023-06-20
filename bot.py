import discord
import discord.ext.commands as commands
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('BOT_TOKEN')

cogs = ["cogs.utils", "cogs.mod", "cogs.greetings", "cogs.error", "cogs.user"]

class MyBot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix, intents=intents, **kwargs)
    
    async def setup_hook(self) -> None:
        for cog in cogs:
            await bot.load_extension(cog)
        print("Loaded all cogs")

    async def on_ready(self):
        print("Bot is ready")
        activity = discord.Game(name="RADAR'S SERVER", type=discord.ActivityType.playing)
        await bot.change_presence(activity=activity)

if __name__ == "__main__":

    bot = MyBot(command_prefix='!', intents=discord.Intents.all())
    bot.run(token)
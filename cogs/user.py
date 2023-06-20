import discord
from discord.ext import commands
from discord import app_commands
from bot import MyBot

class User(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot

    @app_commands.command(name="botinfo", description="Get info about bot")
    async def botinfo(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Bot Info", description="**RADBOT is a multipurpose bot for multipurpose Servers**", colour=0xff7700)
        embed.set_author(name="RADBOT", url="https://github.com/HamzaMemon-G/Radbot", icon_url="https://i.imgur.com/Zn06dLv.png")
        embed.add_field(name="Made By", value="radar.dev", inline=True)
        embed.add_field(name="API", value="Discord.py", inline=True)
        embed.add_field(name="Language Support", value="English", inline=True)
        embed.add_field(name="Host", value="No Host", inline=True)
        embed.set_image(url="https://i.imgur.com/Zn06dLv.png")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: MyBot):
    await bot.add_cog(User(bot))
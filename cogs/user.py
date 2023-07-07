import discord
from discord.ext import commands
from discord import app_commands
from bot import MyBot
from cogs.extra import allcommandslist, usercommandslist, url, iconurl

class User(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot

    @app_commands.command(name="botinfo", description="Get info about bot")
    async def botinfo(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Bot Info", description="**RADBOT is a multipurpose bot for multipurpose Servers**", colour=0xff7700)
        embed.set_author(name="RADBOT", url=url, icon_url=iconurl)
        embed.add_field(name="Made By", value="radar.dev", inline=True)
        embed.add_field(name="API", value="Discord.py", inline=True)
        embed.add_field(name="Language Support", value="English", inline=True)
        embed.add_field(name="Host", value="No Host", inline=True)
        embed.set_image(url=iconurl)
        embed.set_footer(text="RADBOT", icon_url=iconurl)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="userinfo", description="Get info about a user")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member):
        embed = discord.Embed(title="User Info", description=f"**About {member}**", colour=0xff7700)
        embed.set_author(name="RADBOT", url=url, icon_url=iconurl)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="User Name", value=member.name, inline=True)
        embed.add_field(name="User Roles", value=", ".join([role.name for role in member.roles]), inline=True)
        embed.add_field(name="User Created At", value=member.created_at.strftime("%a, %b %d, %Y %I:%M %p"), inline=True)
        embed.add_field(name="User Joined At", value=member.joined_at.strftime("%a, %b %d, %Y %I:%M %p"), inline=True)
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(text="RADBOT", icon_url=iconurl)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: MyBot):
    await bot.add_cog(User(bot))
import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import random
from bot import MyBot
from cogs.extra import allcommandslist, usercommandslist,url, iconurl
import asyncio
import datetime
import typing
import pytz

class Utils(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot

    @app_commands.command(name="announce", description="Announce a message to a channel")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "SR.Admin")
    async def announce(self, interaction: discord.Interaction, channel: discord.TextChannel, embed: bool, role: Optional[discord.Role] = None, message: Optional[str] = None, title: Optional[str] = None, url: Optional[str] = None, author: Optional[str] = None, image: Optional[str] = None, r: Optional[int] = 255, g: Optional[int] = 119, b: Optional[int] = 0):
        
        await interaction.response.defer(thinking=True)
        message = message.replace("\\n", "\n")

        if embed == True:
            embed = discord.Embed(title=title, url=url, description=message, color=discord.Color.from_rgb(r, g, b))
            if message is None:
                embed.description = ""

            if author is None:
                embed.set_footer(text=f"announcement by {interaction.user}")
            else:
                embed.set_footer(text=f"announcement by {author}")

            if image is not None:
                image_links = image.split(",")
                for link in image_links:
                    embed.set_image(url=link.strip())
            if role is not None:
                mention = role.mention
                embed=embed
                await channel.send(content=mention, embed=embed)
            else:
                await channel.send(embed=embed)
        else:
            if role is not None:
                mention = role.mention
                paragraphs = message.split("\n")
                for paragraph in paragraphs:
                    await channel.send(f"{mention}\n{paragraph}")
            else:
                await channel.send(content=message)

        await interaction.followup.send("Announced your message", ephemeral=True)

    @app_commands.command(name="poll", description="Create a poll")
    @app_commands.describe(duration="When the poll should end (YYYY-MM-DD HH:MM:SS)")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "SR.Admin")
    async def poll(self, interaction: discord.Interaction, *, title: str, question: str, duration: str, option1: str, option2: str, r: Optional[int]=255, g: Optional[int]=119, b: Optional[int]=0):
        embed = discord.Embed(title=title, description=question, color=discord.Color.from_rgb(r, g, b))

        duration = datetime.datetime.strptime(duration, "%Y-%m-%d %H:%M:%S")
        user_timezone = pytz.timezone("Asia/Kolkata")
        duration = user_timezone.localize(duration)
        duration_utc = duration.astimezone(pytz.utc)

        end_time_utc = duration_utc.strftime("%Y-%m-%d %I:%M:%S %p %Z")
        end_time_local = duration.astimezone(user_timezone).strftime("%Y-%m-%d %I:%M:%S %p %Z")
        embed.set_footer(text=f"Poll created by {interaction.user} | Ends at ({end_time_local}) ({end_time_utc})")

        embed.add_field(name="Option 1", value=option1, inline=False)
        embed.add_field(name="Option 2", value=option2, inline=False)

        message = await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Poll created!", ephemeral=True)

        option_emojis = ["1️⃣", "2️⃣"]
        for i in range(2):
            await message.add_reaction(option_emojis[i])

        now = datetime.datetime.now(pytz.utc)
        delta = duration_utc - now
        await asyncio.sleep(delta.total_seconds())

        message = await interaction.channel.fetch_message(message.id)

        counts = [0, 0]
        for reaction in message.reactions:
            if reaction.emoji in option_emojis:
                index = option_emojis.index(reaction.emoji)
                counts[index] = reaction.count - 1

        if counts[0] > counts[1]:
            result_message = f"The winner is **{option1}** with {counts[0]} votes!"
        elif counts[1] > counts[0]:
            result_message = f"The winner is **{option2}** with {counts[1]} votes!"
        else:
            result_message = f"The poll ended in a tie with **{counts[0]}** votes each!"

        await interaction.channel.send(result_message)

    @app_commands.command(name="synccommands", description="Sync all the commands")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def sync_command(self, interaction: discord.Interaction):
        await self.bot.tree.sync()
        await interaction.response.send_message("Synced all the commands", ephemeral=True)    

    @app_commands.command(name="status", description="test command")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "SR.Admin")
    async def Status(self, interaction: discord.Interaction):
        await interaction.response.send_message("Bot is working fine", ephemeral=True)

    @app_commands.command(name="say", description="Say a message")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "SR.Admin")
    async def say(self, interaction: discord.Interaction, channel: discord.TextChannel, embed: bool, *, message: str, title: Optional[str]=None, r: Optional[int]=255, g: Optional[int]=119, b: Optional[int]=0):
        
        if embed == True:
            embed = discord.Embed(title=title, description=message, color=discord.Color.from_rgb(r, g, b))
            embed.set_footer(text=f"Message by {interaction.user}")
            await interaction.response.defer(thinking=True)
            await channel.send(embed=embed)
        else:
            await interaction.response.defer(thinking=True)
            await channel.send(message)
            await interaction.followup.send("Message has been sent", ephemeral=True)

    @app_commands.command(name="help", description="Get help about commands")
    async def help(self, interaction: discord.Interaction):

        if any(role.name in ["Staff", "Moderator", "SR.Moderator", "Admin", "SR.Admin"] for role in interaction.user.roles):
            embed = discord.Embed(title="Help (Staff)", description="", colour=0xff7700)
            embed.set_author(name="RADBOT", url=url, icon_url=iconurl)
            embed.set_thumbnail(url=iconurl)
            embed.set_footer(text="RADBOT", icon_url=iconurl)
            for command in allcommandslist:
                embed.description += f"`/{command['name']}` - {command['description']}\n"
        else:
            user_commands = [command for command in usercommandslist if not command.get("staff_only")]
            embed = discord.Embed(title="Help", description="", colour=0xff7700)
            embed.set_author(name="RADBOT", url=url, icon_url=iconurl)
            embed.set_thumbnail(url=iconurl)
            embed.set_footer(text="RADBOT", icon_url=iconurl)
            for command in user_commands:
                embed.description += f"`/{command['name']}` - {command['description']}\n"

        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    @app_commands.command(name="giveaway", description="Start a giveaway")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "SR.Admin")
    async def giveaway(self, interaction: discord.Interaction, channel: discord.TextChannel, description: str, duration: int, winners: int, *, prize: str, host: Optional[discord.Member] = None):
        
        await interaction.response.defer(thinking=True)
        if host is None:
            host_mention = interaction.user.mention
        else:
            host_mention = host.mention

        embed = discord.Embed(title="Giveaway", description=description, color=discord.Color.from_rgb(255, 119, 0))        
        embed.add_field(name="Prize", value=prize)
        embed.add_field(name="Duration", value=f"{duration} seconds")
        embed.add_field(name="Winners", value=winners)
        embed.add_field(name="Hosted by", value=host_mention)
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)
        embed.set_footer(text=f"Ends at {end_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        message = await channel.send(embed=embed)
        await message.add_reaction("🎉")
        await interaction.followup.send("Giveaway created!", ephemeral=True)

        duration = datetime.timedelta(seconds=duration)
        await asyncio.sleep(duration.total_seconds())
        message = await channel.fetch_message(message.id)
        users = [user async for user in message.reactions[0].users()]
        users.remove(self.bot.user)

        if len(users) == 0:
            await channel.send("**No one entered the giveaway!**")
        else:
            users = random.sample(users, winners)
            winner_list = ""
            for user in users:
                winner_list += f"{user.mention}\n"
            await channel.send(f"**Congratulations {winner_list}! You won the giveaway for {prize}!**")

async def setup(bot: MyBot):
    await bot.add_cog(Utils(bot))
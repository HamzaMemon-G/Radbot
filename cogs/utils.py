import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import random
from bot import MyBot
from cogs.extra import allcommandslist, usercommandslist,url, iconurl
import asyncio
import datetime

class Utils(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot

    @app_commands.command(name="announce", description="Announce a message to a channel")
    @app_commands.checks.has_any_role("STAFF", "MODERATOR", "SR.MODERATOR", "ADMIN", "SR.ADMIN")
    async def announce(self, interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role, embed: bool, *, message: str, title: Optional[str]=None, author: Optional[str]=None,r: Optional[int]=255, g: Optional[int]=119, b: Optional[int]=0):
    
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
            await interaction.response.defer(thinking=True)
            await channel.send(role.mention)
            await channel.send(message)
        await interaction.followup.send("Announced your message", ephemeral=True)

    @app_commands.command(name="poll", description="Create a poll")
    @app_commands.checks.has_any_role("STAFF", "MODERATOR", "SR.MODERATOR", "ADMIN", "SR.ADMIN")
    async def poll(self, interaction: discord.Interaction, *, title: str, question: str, reaction1: str, reaction2: str, duration: int, r: Optional[int]=255, g: Optional[int]=119, b: Optional[int]=0):
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

        if winner == "Tie":
            result_message = "The poll ended in a tie!"
        else:
            result_message = f"The winner is {winner} with {max(count1, count2)} votes!"

        await interaction.channel.send(result_message)

    @app_commands.command(name="synccommands", description="Sync all the commands")
    @app_commands.checks.has_any_role("STAFF", "MODERATOR", "SR.MODERATOR", "ADMIN", "SR.ADMIN")
    async def sync_command(self, interaction: discord.Interaction):
        await self.bot.tree.sync()
        await interaction.response.send_message("Synced all the commands", ephemeral=True)    

    @app_commands.command(name="status", description="test command")
    @app_commands.checks.has_any_role("STAFF", "MODERATOR", "SR.MODERATOR", "ADMIN", "SR.ADMIN")
    async def Status(self, interaction: discord.Interaction):
        await interaction.response.send_message("Bot is working fine", ephemeral=True)

    @app_commands.command(name="say", description="Say a message")
    @app_commands.checks.has_any_role("STAFF", "MODERATOR", "SR.MODERATOR", "ADMIN", "SR.ADMIN")
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

        if any(role.name in ["STAFF", "MODERATOR", "SR.MODERATOR", "ADMIN", "SR.ADMIN"] for role in interaction.user.roles):
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
    @app_commands.checks.has_any_role("STAFF", "MODERATOR", "SR.MODERATOR", "ADMIN", "SR.ADMIN")
    async def giveaway(self, interaction: discord.Interaction, channel: discord.TextChannel, description: str, duration: int, winners: int, *, prize: str):
        embed = discord.Embed(title="Giveaway", description=description, color=discord.Color.from_rgb(255, 119, 0))        
        embed.add_field(name="Prize", value=prize)
        embed.add_field(name="Duration", value=f"{duration} seconds")
        embed.add_field(name="Winners", value=winners)
        embed.add_field(name="Hosted by", value=interaction.user.mention)
        end_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=duration)
        embed.set_footer(text=f"Ends at {end_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        message = await channel.send(embed=embed)
        await message.add_reaction("🎉")
        await interaction.response.send_message("Giveaway created!", ephemeral=True)

        duration = datetime.timedelta(seconds=duration)
        await asyncio.sleep(duration.total_seconds())
        message = await channel.fetch_message(message.id)
        users = [user async for user in message.reactions[0].users()]
        users.remove(self.bot.user)
        users = random.sample(users, winners)

        if len(users) == 0:
            await channel.send("No one won the giveaway!")
        else:
            winner_list = ""
            for user in users:
                winner_list += f"{user.mention}\n"
            await channel.send(f"**Congratulations {winner_list}! You won the giveaway for {prize}!**")

async def setup(bot: MyBot):
    await bot.add_cog(Utils(bot))
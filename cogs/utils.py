import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
import asyncio
from datetime import timedelta
from bot import MyBot


class Utils(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot

    @app_commands.command(name="announce", description="Announce a message to a channel")
    @app_commands.checks.has_role("Staff")
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
            await channel.send(message)
            await channel.send(role.mention)
        await interaction.followup.send("Announced your message" , ephemeral=True)

    @app_commands.command(name="poll", description="Create a poll")
    @app_commands.checks.has_role("Staff")
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

    @app_commands.command(name="synccommand", description="Sync all the commands")
    async def sync_command(self, interaction: discord.Interaction):
        await self.bot.tree.sync()
        await interaction.response.send_message("Synced all commands", ephemeral=True)    

    @app_commands.command(name="test", description="test command")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Test command is working", ephemeral=True)

async def setup(bot: MyBot):
    await bot.add_cog(Utils(bot))
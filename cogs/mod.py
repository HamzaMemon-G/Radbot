import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional
from datetime import timedelta
from bot import MyBot


class Mod(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kick a user from the server")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, *, reason: str):
        await user.kick(reason=reason)
        await interaction.channel.send(f"Kicked {user.mention} for **{reason}**")
        await interaction.response.send_message(f"Kicked {user} for **{reason}**", ephemeral=True)
    
    @app_commands.command(name="warn", description="Warn a user")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, *, reason: str):
        await interaction.response.defer(thinking=True)
        await interaction.channel.send(f"Warned {user.mention} for **{reason}**")
        await interaction.followup.send(f"Warned {user} for **{reason}**", ephemeral=True)

    @app_commands.command(name="whois", description="Get information about a user")
    async def whois(self, interaction: discord.Interaction, user: discord.Member):
        embed = discord.Embed(title=f"{user}", description=f"Information about {user.mention}", color=user.color)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Joined at", value=user.joined_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
        embed.add_field(name="Created at", value=user.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
        embed.set_thumbnail(url=user.display_avatar)
        embed.set_footer(text=f"Requested by {interaction.user}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="purge", description="Purge messages in a channel")
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Purged {amount} messages", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a user from the server")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, *, reason: str):
        await user.ban(reason=reason)
        await interaction.channel.send(f"Banned {user.mention} for **{reason}**")
        await interaction.response.send_message(f"Banned {user} for **{reason}**", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user from the server")
    async def unban(self, interaction: discord.Interaction, user: discord.User, *, reason: str):
        member = await bot.fetch_user(user.id)
        await interaction.guild.unban(member, reason=reason)
        await interaction.channel.send(f"Unbanned {user.mention} for **{reason}**")
        dm_channel = await user.create_dm()
        await dm_channel.send(f"You have been unbanned from **{interaction.guild.name}** for **{reason}**")
    
    @app_commands.command(name="timeout", description="Timeout a user")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minitues: int, *, reason: str):
        delta = timedelta(minutes=minitues)
        await member.timeout(delta, reason=reason)
        await interaction.channel.send(f"Timed out {member.mention} for **{reason}**")
        await interaction.response.send_message(f"Timed out {member} for **{reason}**", ephemeral=True)

async def setup(bot: MyBot):
    await bot.add_cog(Mod(bot))
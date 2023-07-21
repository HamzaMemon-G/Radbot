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
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, *, reason: str):
        await user.kick(reason=reason)
        await interaction.channel.send(f"Kicked {user.mention} for **{reason}**")
        await interaction.response.send_message(f"Kicked {user} for **{reason}**", ephemeral=True)

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to kick that user", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to kick that user", ephemeral=True)
        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Please provide all the required arguments", ephemeral=True)
        elif isinstance(error, discord.NotFound):
            await interaction.response.send_message("User not found", ephemeral=True)
    
    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, *, reason: str):
        await interaction.response.defer(thinking=True)
        await interaction.channel.send(f"Warned {user.mention} for **{reason} by {interaction.user}**")
        await interaction.followup.send(f"Warned {user} for **{reason}**", ephemeral=True)

    @warn.error
    async def warn_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to warn that user", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to warn that user", ephemeral=True)

    @app_commands.command(name="whois", description="Get information about a user")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def whois(self, interaction: discord.Interaction, user: discord.Member):
        embed = discord.Embed(title=f"{user}", description=f"Information about {user.mention}", color=user.color)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Joined at", value=user.joined_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
        embed.add_field(name="Created at", value=user.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=False)
        embed.set_thumbnail(url=user.display_avatar)
        embed.set_footer(text=f"Requested by {interaction.user}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @whois.error
    async def whois_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to get information about that user", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to get information about that user", ephemeral=True)
        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Please provide all the required arguments", ephemeral=True)

    @app_commands.command(name="purge", description="Purge messages in a channel")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Purged {amount} messages", ephemeral=True)

    @purge.error
    async def purge_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to purge messages", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to purge messages", ephemeral=True)
        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Please provide all the required arguments", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a user from the server")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, *, reason: str):
        await user.ban(reason=reason)
        await interaction.channel.send(f"Banned {user.mention} for **{reason}**")
        await interaction.response.send_message(f"Banned {user} for **{reason}**", ephemeral=True)

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to ban that user", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to ban that user", ephemeral=True)
        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Please provide all the required arguments", ephemeral=True)
        elif isinstance(error, discord.NotFound):
            await interaction.response.send_message("User not found", ephemeral=True)

    @app_commands.command(name="unban", description="Unban a user from the server")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def unban(self, interaction: discord.Interaction, user: discord.User, *, reason: str):
        member = await bot.fetch_user(user.id)
        await interaction.guild.unban(member, reason=reason)
        await interaction.channel.send(f"Unbanned {user.mention} for **{reason}**")
        dm_channel = await user.create_dm()
        await dm_channel.send(f"You have been unbanned from **{interaction.guild.name}** for **{reason}**")
        
    @unban.error
    async def unban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to unban that user", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to unban that user", ephemeral=True)
        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Please provide all the required arguments", ephemeral=True)
        elif isinstance(error, discord.NotFound):
            await interaction.response.send_message("User not found", ephemeral=True)   
    
    @app_commands.command(name="timeout", description="Timeout a user")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, minitues: int, *, reason: str):
        delta = timedelta(minutes=minitues)
        await member.timeout(delta, reason=reason)
        await interaction.channel.send(f"Timed out {member.mention} for **{reason}**")
        await interaction.response.send_message(f"Timed out {member} for **{reason}**", ephemeral=True)
    
    @timeout.error
    async def timeout_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to timeout that user", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to timeout that user", ephemeral=True)
        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Please provide all the required arguments", ephemeral=True)
        elif isinstance(error, discord.NotFound):
            await interaction.response.send_message("User not found", ephemeral=True)        

    @app_commands.command(name="mute", description="Mute a user")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")   
    async def mute(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        await member.add_roles(discord.utils.get(member.guild.roles, name="Muted"), reason=reason)
        await interaction.channel.send(f"Muted {member.mention} for **{reason}**")
        await interaction.response.send_message(f"Muted {member} for **{reason}**", ephemeral=True)

    @mute.error
    async def mute_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to mute that user", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to mute that user", ephemeral=True)
        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Please provide all the required arguments", ephemeral=True)
        elif isinstance(error, discord.NotFound):
            await interaction.response.send_message("User not found", ephemeral=True)
            
    @app_commands.command(name="unmute", description="Unmute a user")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def unmute(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        await member.remove_roles(discord.utils.get(member.guild.roles, name="Muted"), reason=reason)
        await interaction.channel.send(f"Unmuted {member.mention} for **{reason}**")
        await interaction.response.send_message(f"Unmuted {member} for **{reason}**", ephemeral=True)
        
    @unmute.error
    async def unmute_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to unmute that user", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to unmute that user", ephemeral=True)
        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Please provide all the required arguments", ephemeral=True)
        elif isinstance(error, discord.NotFound):
            await interaction.response.send_message("User not found", ephemeral=True)

    @app_commands.command(name="lockvc", description="Lock a voice channel")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def voicelock(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        await channel.set_permissions(interaction.guild.default_role, connect=False)
        await interaction.response.send_message("Locked the voice channel", ephemeral=True)

    @voicelock.error
    async def voicelock_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to lock that voice channel", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to lock that voice channel", ephemeral=True)
        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Please provide all the required arguments", ephemeral=True)
        elif isinstance(error, discord.NotFound):
            await interaction.response.send_message("Voice channel not found", ephemeral=True)
        
    @app_commands.command(name="unlockvc", description="Unlock a voice channel")
    @app_commands.checks.has_any_role("Staff", "Moderator", "SR.Moderator", "Admin", "Sr.Admin")
    async def voiceunlock(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        await channel.set_permissions(interaction.guild.default_role, connect=True)
        await interaction.response.send_message("Unlocked the voice channel", ephemeral=True)

    @voiceunlock.error
    async def voiceunlock_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message("I don't have permission to unlock that voice channel", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await interaction.response.send_message("An error occured while trying to unlock that voice channel", ephemeral=True)
        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Please provide all the required arguments", ephemeral=True)
        elif isinstance(error, discord.NotFound):
            await interaction.response.send_message("Voice channel not found", ephemeral=True)

async def setup(bot: MyBot):
    await bot.add_cog(Mod(bot))
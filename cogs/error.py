import discord
from discord.ext import commands
from discord import app_commands
from bot import MyBot
import random

class Error(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):

        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("Opps you don't have permission, go die!", ephemeral=True)

        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message("Wait it's on cooldown Stupid!", ephemeral=True)

        elif isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("Command failed because of your dumbness", ephemeral=True)

        elif isinstance(error, app_commands.CommandSyncFailure):
            await interaction.response.send_message("Command synced failed because you don't know how to play piano", ephemeral=True)

        elif isinstance(error, app_commands.UserInputError):
            await interaction.response.send_message("Input Error, Because your failure", ephemeral=True)
        
        elif isinstance(error, app_commands.CommandNotFound):
            await interaction.response.send_message("Command not found, There is not command like that", ephemeral=True)

        elif isinstance(error, app_commands.MissingRequiredArgument):
            await interaction.response.send_message("Missing required argument, You are missing argument like your brain", ephemeral=True)
        
        elif isinstance(error, app_commands.TooManyArguments):
            await interaction.response.send_message("Too many arguments, You are giving too many arguments", ephemeral=True)

async def setup(bot: MyBot):
    await bot.add_cog(Error(bot))
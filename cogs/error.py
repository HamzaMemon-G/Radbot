import discord
from discord.ext import commands
from discord import app_commands
from bot import MyBot
import random

missingrole_error = ["Missing role like your brain", "You don't have cool roles to use this command because your loser", "You can't use this because your failure"]
cooldown_erorr = ["Wait idiot command is on cooldown 😡", "Have some patience", "Why in hurry ?", "I am tired I will not run command"]
failure_erorr = ["Command failed because your disappointment like Steven", "Command fail because you are Dumb", "Command failed because you work in failure management", "Command failed because you can't play piano"]
input_error = ["Can't write a single command your cousin RADAR wrote a discord bot when he was in Nursery", "Wrong input", "Wrong input nobody get this error why so dumb"]

class Error(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):

        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(random.choices(missingrole_error)[0], ephemeral=True)

        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(random.choices(cooldown_erorr)[0], ephemeral=True)

        elif isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(random.choices(failure_erorr)[0], ephemeral=True)

        elif isinstance(error, app_commands.UserInputError):
            await interaction.response.send_message(random.choices(input_error)[0], ephemeral=True)

        elif isinstance(error, app_commands.CommandSyncFailure):
            await interaction.response.send_message("Command synced failed", ephemeral=True)


async def setup(bot: MyBot):
    await bot.add_cog(Error(bot))
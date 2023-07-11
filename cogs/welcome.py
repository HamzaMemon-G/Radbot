import discord
from discord.ext import commands
from discord import app_commands
from bot import MyBot

class Welcome(welcome.cog):
    def __init__ (self, bot: MyBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        embed = discord.embed(title = "Welcome👋", description=f"{member.mention} thank you for joining the Odyssey VTC Discord server!\n Feel free to look around and join our community.")
        embed.add_field(name="> **Wanna join the Odyssey VTC?**", value="You can apply [here](https://truckersmp.com/user/5132120)")
        embed.add_field(name="> **Have any questions?**", value=f"Feel free to ask in {self.bot.get_channel(1128020624267280424).mention}")
        embed.set_thumbnail(url=member.avatar)
        embed.set_image(url="https://discord.gg/KACvUNyyaY")
        embed.set_footer(name="Odyssey VTC Staff", url="https://discord.gg/KACvUNyyaY")
        channel = self.bot.get_channel(1128020624267280424, 1128017313908670464)
        await channel.send(embed=embed)

async def setup(bot: MyBot):
    await bot.add_cog(Welcome(bot))
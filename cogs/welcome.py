import discord
from discord.ext import commands
from discord import app_commands
from bot import MyBot

class Welcome(commands.Cog):
    def __init__ (self, bot: MyBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        embed = discord.Embed(title = "Welcome👋", description=f"{member.mention} thank you for joining the Odyssey VTC Discord server!\n\n Feel free to look around and join our community.", color=discord.Color.from_rgb(255, 119, 0))
        embed.add_field(name="> **Wanna join the Odyssey VTC?**", value="**You can apply [here](https://truckersmp.com/user/5132120)**")
        embed.add_field(name="> **Have any questions?**", value=f"**Feel free to ask in {self.bot.get_channel(1128020624267280424).mention}**")
        embed.set_thumbnail(url=member.avatar)
        embed.set_image(url="https://i.imgur.com/oYhNR6h.png")
        embed.set_footer(text="Odyssey VTC Staff", icon_url="https://i.imgur.com/YRjbLdD.png")
        channel1 = self.bot.get_channel(1128017313908670464)
        channel2 = self.bot.get_channel(1128020624267280424)
        await channel1.send(embed=embed)
        await channel2.send(embed=embed)

async def setup(bot: MyBot):
    await bot.add_cog(Welcome(bot))
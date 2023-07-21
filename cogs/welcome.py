import discord
from discord.ext import commands
from discord import app_commands
from bot import MyBot

class Welcome(commands.Cog):
    def __init__ (self, bot: MyBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(980707987716997160)
        embed = discord.Embed(title = "Welcome👋", description=f"{member.mention} thank you for joining the RADAR'S SERVER Discord server!\n\n Feel free to look around and join our community.", color=discord.Color.from_rgb(255, 119, 0))
        embed.add_field(name="> **Wanna join the RADAR'S SERVER?**", value=f"**You can get the ip here {self.bot.get_channel(1006098590025928755).mention}**", inline=True)
        embed.add_field(name="> **Have any questions?**", value=f"**Feel free to ask in {self.bot.get_channel(992123833203036270).mention}**", inline=True)
        embed.set_thumbnail(url=member.avatar)
        embed.set_image(url="https://i.imgur.com/zxnfIg2.png")
        embed.set_footer(text="RADAR'S SERVER Staff", icon_url="https://i.imgur.com/zxnfIg2.png")
        await channel.send(embed=embed)
        await channel.send(f"**Welcome {member.mention} to RADAR'S SERVER**")
        await member.send(embed=embed)
        await member.send(f"**Welcome {member.mention} to RADAR'S SERVER**")

async def setup(bot: MyBot):
    await bot.add_cog(Welcome(bot))
import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=['latency'], usage="tells bot's latency", help="/ping")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ping(self, ctx):
        embed = discord.Embed()
        embed.color = 0x2f3136
        embed.description = f"Pong! 🏓 Latency: **{round(self.bot.latency * 1000)}ms**"
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))

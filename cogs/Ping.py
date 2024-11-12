import discord
from discord.ext import commands

class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @discord.command(name="ping", description="Returns the bot's ping")
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"My ping is {round(self.bot.latency*1000)}ms")


def setup(bot):
    bot.add_cog(Ping(bot))

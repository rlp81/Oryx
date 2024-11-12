import discord
from discord.ext import commands
import time
import datetime
import platform


def get_lib():
    return "Py-cord " + str(discord.__version__)


def get_kernel():
    return "Linux " + str(platform.release()).split("-")[0]


def get_version():
    return "Python " + platform.python_version()


def get_uptime():
    days = datetime.datetime.now().day - datetime.datetime.fromtimestamp(
        datetime.datetime.now().timestamp() - time.monotonic()).day
    hrs = datetime.datetime.now().hour - datetime.datetime.fromtimestamp(
        datetime.datetime.now().timestamp() - time.monotonic()).hour
    mins = datetime.datetime.now().minute - datetime.datetime.fromtimestamp(
        datetime.datetime.now().timestamp() - time.monotonic()).minute
    secs = datetime.datetime.now().second - datetime.datetime.fromtimestamp(
        datetime.datetime.now().timestamp() - time.monotonic()).second
    if days < 0:
        days = days*-1
    if hrs < 0:
        hrs = hrs*-1
    if mins < 0:
        mins = mins*-1
    if secs < 0:
        secs = secs*-1
    return f"{days} days, {hrs} hours, {mins} minutes, {secs} seconds"


class Info(discord.Cog):

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @discord.command(name="info", description="Information about the bot")
    async def _info(self, ctx: discord.ApplicationContext):
        emb = discord.Embed(title="Bot Information")
        emb.add_field(name="Created by", value="rlp81")
        emb.add_field(name="Created At", value=str(self.bot.user.created_at.date()))
        emb.add_field(name="Username", value=str(self.bot.user))
        emb.add_field(name="Library", value=get_lib())
        emb.add_field(name="Platform", value=get_kernel())
        emb.add_field(name="Python Version", value=get_version())
        emb.add_field(name="Uptime", value=get_uptime())
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.respond(embed=emb)


def setup(bot):
    bot.add_cog(Info(bot))

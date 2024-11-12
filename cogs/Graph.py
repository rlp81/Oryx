import discord
from discord.ext import commands
import matplotlib
import matplotlib.pyplot as plt
import json
import datetime
import os


class Graph(commands.Cog):

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    gcmd = discord.SlashCommandGroup(name="graph", description="Commands related to graphing and data visualization")

    @gcmd.command(name="activity", description="Server activity graph")
    async def activity(self, ctx: discord.ApplicationContext):
        with open("graph.json", "r") as f:
            grph = json.load(f)
        if str(ctx.guild.id) in grph:
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            days = (datetime.date(year, month+1, 1) - datetime.date(year, month, 1)).days
            #print(days)
            dates = []
            nums = []
            for i in range(days):
                i=i+1
                dat = datetime.date(year, month, i)
                date = str(dat).replace("-", "_")
                if not date in grph[str(ctx.guild.id)]:
                    msgs = 0
                else:
                    msgs = grph[str(ctx.guild.id)][date]
                #msgs = random.randint(10, 300)
                dates.append(str(dat))
                nums.append(msgs)
            plt.figure(figsize=(14, 9))
            plt.plot(dates, nums, color='red', linewidth=2)
            plt.title("Activity")
            plt.xlabel("Date")
            plt.ylabel("Messages")
            #date_form = matplotlib.dates.DateFormatter("%Y-%m-%d")
            plt.gcf().autofmt_xdate()
            plt.savefig(f"{os.getcwd()}/plot.png")
            await ctx.respond(file=discord.File(f"{os.getcwd()}/plot.png"))
            os.remove(f"{os.getcwd()}/plot.png")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        if message.author.bot:
            return
        if not message.id:
            return
        with open("graph.json", "r") as f:
            grph = json.load(f)
        date = str(datetime.datetime.now().date()).replace("-", "_")
        if str(message.guild.id) in grph:
            if date in grph[str(message.guild.id)]:
                grph[str(message.guild.id)][date] = int(grph[str(message.guild.id)][date]) + 1
            else:
                grph[str(message.guild.id)][date] = 1
        else:
            grph[str(message.guild.id)] = {
                date: 1
            }
        with open("graph.json", "w") as f:
            json.dump(grph, f, indent=4)


def setup(bot):
    bot.add_cog(Graph(bot))

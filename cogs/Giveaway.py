import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from datetime import datetime, timedelta
import json
import random
from pytimeparse.timeparse import timeparse


def parse(msg):
    try:
        num = timeparse(msg)
        return num
    except:
        return "ERROR"


def get_id():
    found = False
    with open("give.json", "r") as f:
        give = json.load(f)
    while found == False:
        num = random.randint(0000, 9999)
        if not str(num) in give:
            return num
        else:
            pass


class Button(discord.ui.Button):

    def __init__(self, cust):
        self.cust = cust
        super().__init__(label="Join Giveaway", style=discord.ButtonStyle.gray, custom_id=str(cust))

    async def callback(self, interaction: discord.Interaction):
        with open("give.json", "r") as f:
            give = json.load(f)
        if str(self.cust) in give:
            if str(interaction.user.id) in give[str(self.cust)]["members"]:
                await interaction.response.send_message("You have already joined the giveaway", ephemeral=True)
            else:
                give[str(self.cust)]["members"].append(str(interaction.user.id))
                with open("give.json", "w") as f:
                    json.dump(give, f, indent=4)
                await interaction.response.send_message("Entered giveaway", ephemeral=True)
        else:
            await interaction.response.send_message("Giveaway not active", ephemeral=True)


class View(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)


class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
        self.check_give.start()

    @commands.Cog.listener()
    async def on_ready(self):
        with open("give.json", "r") as f:
            give: dict = json.load(f)
        view = View()
        for i, v in give.items():
            view.add_item(Button(i))
        self.bot.add_view(view=view)

    @tasks.loop(seconds=10)
    async def check_give(self):
        with open("give.json", "r") as f:
            give: dict = json.load(f)
        now = datetime.now().timestamp()
        dele = []
        for i, v in give.items():
            try:
                channel = await self.bot.fetch_channel(int(give[i]["channel"]))
                members = list(give[i]["members"])
                if channel:
                    when = give[i]["when"]
                    message: discord.Message = await channel.fetch_message(int(give[i]["message"]))
                    if message:
                        reason = give[i]["reason"]
                        if now >= int(when):
                            if i not in dele:
                                view = discord.ui.View.from_message(message)
                                view.disable_all_items()
                                if members == []:
                                    await channel.send(f"**Giveaway**\nNo winner")
                                    emb = discord.Embed(title="Giveaway", description=f"Prize: {reason}",
                                                        color=discord.Color.embed_background())
                                    emb.add_field(name="Winner", value=f"None", inline=False)
                                    await message.edit(embed=emb, view=view)
                                    dele.append(i)
                                else:
                                    winner = int(random.choice(members))
                                    win = await self.bot.fetch_user(winner)
                                    await channel.send(f"**Giveaway**\n{win.mention} has won {reason}!")
                                    emb = discord.Embed(title="Giveaway", description=f"Prize: {reason}", color=discord.Color.embed_background())
                                    emb.add_field(name="Winner", value=f"{win.mention}", inline=False)
                                    dele.append(i)
                                    await message.edit(embed=emb, view=view)
            except:
                pass
        for i in dele:
            give.pop(str(i))
        with open("give.json", "w") as f:
            json.dump(give, f, indent=4)

    @discord.slash_command(name="giveaway", description="Starts a giveaway")
    @has_permissions(manage_channels=True)
    async def giveaway(self, ctx: discord.ApplicationContext,
                  item: str, time: str, channel: discord.TextChannel = None, mention: discord.Role = None):
        with open("give.json", "r") as f:
            give = json.load(f)
        num = get_id()
        delta = parse(time)
        if delta == "ERROR" or delta is None:
            await ctx.respond("Invalid time input\nSupported time inputs: Seconds, Minutes, Hours, Days, and Weeks.\ne.g. 3d/3 days")
            return
        else:
            await ctx.respond("Generating..", ephemeral=True)
            now = datetime.now().timestamp()
            when = now + delta
            end = datetime.fromtimestamp(round(when))
            if not channel:
                channel = ctx.channel
            view = View()
            view.add_item(Button(num))
            emb = discord.Embed(title="Giveaway", description=f"Prize: {item}", color=discord.Color.embed_background())
            emb.add_field(name="Ends at", value=f"{end} CST")
            emb.set_footer(text=f"Started by {ctx.author}")
            if mention:
                if mention.is_default():
                    message = await channel.send(f"{mention}", embed=emb, view=view)
                else:
                    message = await channel.send(f"{mention.mention}", embed=emb, view=view)
            else:
                message = await channel.send(embed=emb, view=view)
            give[str(num)] = {
                "message": message.id,
                "channel": channel.id,
                "members": [],
                "when": when,
                "reason": item
            }
            with open("give.json", "w") as f:
                json.dump(give,f,indent=4)

def setup(bot):

    bot.add_cog(giveaway(bot))

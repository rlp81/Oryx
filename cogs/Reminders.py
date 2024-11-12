import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import json
import random
from pytimeparse.timeparse import timeparse

async def get_rems(ctx: discord.AutocompleteContext):
    item_list = []
    with open("reminders.json", "r") as f:
        rems = json.load(f)
    for i, v in rems[str(ctx.interaction.guild_id)].items():
        item_list.append(i)
    items = []
    for item in item_list:
        value_lower, item_lower = str(ctx.value).lower(), str(item).lower()
        if value_lower in item_lower or ctx.value == '':
            items.append(item)
    return [value for value in items]

def parse(msg):
    try:
        num = timeparse(msg)
        return num
    except:
        return "ERROR"

def get_id():
    found = False
    with open("reminders.json", "r") as f:
        rems = json.load(f)
    while found == False:
        num = random.randint(000,999)
        if not str(num) in rems:
            return num
        else:
            pass

async def get_pings(ctx: discord.AutocompleteContext):
    mention = ctx.options["mention"]
    if mention == "member":
        return discord.Member
    if mention == "role":
        return discord.Role


class reminders(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
        self.remind.start()

    @tasks.loop(seconds=5)
    async def remind(self):
        with open("reminders.json", "r") as f:
            rems: dict = json.load(f)
        now = datetime.now().timestamp()
        dele = []
        for i in rems:
            for reminder, v in rems[i].items():
                try:
                    channel = self.bot.get_channel(int(rems[i][str(reminder)]["channel"]))
                    member = await self.bot.fetch_user(int(rems[i][str(reminder)]["member"]))
                    if channel and member:
                        looping = rems[i][str(reminder)]["looping"]
                        when = rems[i][str(reminder)]["when"]
                        reason = rems[i][str(reminder)]["reason"]
                        if now >= int(when):
                            await channel.send(f"**Reminder** {member.mention}\n{reason}")
                            if looping == False:
                                dele.append([i, reminder])
                            else:
                                delta = parse(looping)
                                if delta == "ERROR":
                                    return
                                when = now + delta
                                rems[i][str(reminder)]["when"] = when
                            with open("reminders.json", "w") as f:
                                json.dump(rems, f, indent=4)
                except:
                    pass
        with open("reminders.json", "r") as f:
            rems: dict = json.load(f)
        for i in dele:
            rems[i[0]].pop(i[1])
        with open("reminders.json", "w") as f:
            json.dump(rems, f, indent=4)

    reminds = discord.SlashCommandGroup(name="reminders", description="Commands related to giving reminders")

    @reminds.command(name="add", description="Adds a new reminder")
    async def add(self, ctx: discord.ApplicationContext,
                  typ: discord.Option(str, name="type", description="Type of reminder", choices=["once", "loop"]),
                  reason: str, time: str, channel: discord.TextChannel = None):
        with open("reminders.json", "r") as f:
            rems = json.load(f)
        num = get_id()
        delta = parse(time)
        if delta == "ERROR" or delta is None:
            await ctx.respond("Invalid time input\nSupported time inputs: Seconds, Minutes, Hours, Days, and Weeks.\ne.g. 3d/3 days")
            return
        else:
            if typ == "loop":
                await ctx.respond("Generating..", ephemeral=True)
                now = datetime.now().timestamp()
                when = now + delta
                if not channel:
                    channel = ctx.channel
                if str(ctx.guild.id) in rems:
                    rems[str(ctx.guild.id)][str(num)] = {
                        "channel": channel.id,
                        "member": ctx.author.id,
                        "looping": time,
                        "when": when,
                        "reason": reason
                    }
                else:
                    rems[str(ctx.guild.id)] = {
                        str(num): {
                            "channel": channel.id,
                            "member": ctx.author.id,
                            "looping": time,
                            "when": when,
                            "reason": reason
                        }
                    }
                with open("reminders.json", "w") as f:
                    json.dump(rems,f,indent=4)
                await ctx.channel.send(f"Created a looping reminder with reason {reason}")
            elif typ == "once":
                await ctx.respond("Generating..", ephemeral=True)
                now = datetime.now().timestamp()
                when = now + delta
                if not channel:
                    channel = ctx.channel
                if str(ctx.guild.id) in rems:
                    rems[str(ctx.guild.id)][str(num)] = {
                        "channel": channel.id,
                        "member": ctx.author.id,
                        "looping": False,
                        "when": when,
                        "reason": reason
                    }
                else:
                    rems[str(ctx.guild.id)] = {
                        str(num): {
                            "channel": channel.id,
                            "member": ctx.author.id,
                            "looping": False,
                            "when": when,
                            "reason": reason
                        }
                    }
                with open("reminders.json", "w") as f:
                    json.dump(rems, f, indent=4)
                await ctx.channel.send(f"Created a one-time reminder with reason {reason}")


    @reminds.command(name="delete", description="Deletes a reminder")
    async def delete(self, ctx: discord.ApplicationContext, reminder: discord.Option(int, name="reminder", description="Reminder ID",
                                            autocomplete=discord.utils.basic_autocomplete(get_rems))):
        with open("reminders.json", "r") as f:
            rems = json.load(f)
        if str(reminder) in rems[str(ctx.guild.id)]:
            rems[str(ctx.guild.id)].pop(str(reminder))
            await ctx.respond(f"Deleted reminder {reminder}")
        else:
            await ctx.respond(f"No reminder {reminder}")
        with open("reminders.json", "w") as f:
            json.dump(rems, f, indent=4)

    @reminds.command(name="list", description="Lists all reminders or lists a reminder's information")
    async def list(self, ctx: discord.ApplicationContext,
                   reminder: discord.Option(int, name="reminder", description="Reminder ID",
                                            autocomplete=discord.utils.basic_autocomplete(get_rems),
                                            required=False) = None):
        with open("reminders.json", "r") as f:
            rems = json.load(f)
        if str(ctx.guild.id) in rems:
            if not reminder:
                desc = ""
                num = len(rems[str(ctx.guild.id)])
                if num == 0:
                    await ctx.respond("No active reminders")
                    return
                for i, v in rems[str(ctx.guild.id)].items():
                    if desc == "":
                        desc += f"{i}"
                    else:
                        desc += f"\n{i}"
                emb = discord.Embed(title="Reminders", description=f"Active reminders: {num}\n{desc}")
                await ctx.respond(embed=emb)
            else:
                if str(reminder) in rems[str(ctx.guild.id)]:
                    rdic = rems[str(ctx.guild.id)][str(reminder)]
                    chan = ctx.guild.get_channel(int(rdic["channel"]))
                    mem = await self.bot.fetch_user(int(rdic["member"]))
                    when = datetime.fromtimestamp(int(rdic["when"]))
                    emb = discord.Embed(title=f"Reminder {reminder}")
                    emb.add_field(name="Channel", value=chan.mention, inline=False)
                    emb.add_field(name="Member", value=mem.mention, inline=False)
                    emb.add_field(name="Looping", value=rdic["looping"], inline=False)
                    emb.add_field(name="When", value=f"{when} CST", inline=False)
                    emb.add_field(name="Reason", value=rdic["reason"], inline=False)
                    await ctx.respond(embed=emb)
                else:
                    await ctx.respond("No such reminder")
        else:
            await ctx.respond("No active reminders")




def setup(bot):

    bot.add_cog(reminders(bot))

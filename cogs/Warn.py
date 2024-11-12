import discord
from discord import option
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import datetime
import json
import random
from pytimeparse.timeparse import timeparse

wset = {
    "1": "none",
    "2": ".m1h",
    "3": ".m1d",
    "4": ".m1w",
    "5": ".k",
    "6": ".b30d",
    "7": ".bf"
}


async def find_id(ctx: discord.AutocompleteContext):
    member = ctx.options["member"]
    #print(member)
    item_list = []
    with open("warns.json", "r") as f:
        warns = json.load(f)
    for i, v in warns[str(ctx.interaction.guild_id)][str(member)].items():
        item_list.append(i)
    items = []
    for item in item_list:
        value_lower, item_lower = str(ctx.value).lower(), str(item).lower()
        if value_lower in item_lower or ctx.value == '':
            items.append(item)
    return [value for value in items]


def get_id(member: discord.Member, warns: dict):
    found = False
    num = 0
    while found is False:
        num = random.randint(0000,9999)
        if not str(num) in warns[str(member.guild.id)][str(member.id)]:
            found = True
    return str(num)


async def warn_check(bot: discord.Bot, guild, member, warns):
    num = len(warns[guild][member])
    #print(num)
    chose = ""
    with open("warnsets.json", "r") as f:
        setts = json.load(f)
    with open("warn.json", "r") as f:
        warn = json.load(f)
    if not guild in warn:
        warn[guild] = {
            member: 0
        }
    elif not member in warn[guild]:
        warn[guild][member] = 0
    if not guild in setts:
        setts[guild] = wset
    with open("warnsets.json", "w") as f:
        json.dump(setts, f, indent=4)
    for i, v in setts[str(guild)].items():
        #print(i)
        if num >= int(i):
            chose = str(i)
    if str(chose) != "" and int(chose) != int(warn[guild][member]):
        pun = setts[guild][str(chose)].lower()
        if pun != "none":
            gld = bot.get_guild(int(guild))
            if gld:
                mem = discord.utils.get(gld.members, id=int(member))
                if pun.startswith(".m"):
                    new = pun.removeprefix(".m")
                    tim = timeparse(new) + datetime.datetime.utcnow().timestamp()
                    un = datetime.datetime.fromtimestamp(tim)
                    try:
                        await mem.timeout(until=un, reason=f"Had {num} warns")
                    except:
                        pass
                if pun.startswith(".k"):
                    try:
                        await mem.kick(reason=f"Had {num} warns")
                    except:
                        pass
                if pun.startswith(".b"):
                    new = pun.removeprefix(".b")
                    if pun.lower() == "f":
                        try:
                            await mem.ban(reason=f"Had {num} warns")
                        except:
                            pass
                    else:
                        tim = timeparse(new) + datetime.datetime.utcnow().timestamp()
                        with open("bans.json", "r") as f:
                            bans = json.load(f)
                        if str(guild) in bans:
                            bans[str(guild)][str(member)] = tim
                        else:
                            bans[str(guild)] = {
                                str(member): tim
                            }
                        with open("bans.json", "w") as f:
                            json.dump(bans, f, indent=4)
                        try:
                            await mem.ban(reason=f"Had {num} warns")
                        except:
                            pass
        warn[guild][member] = int(chose)
        with open("warn.json", "w") as f:
            json.dump(warn, f, indent=4)



class Warn_System(discord.Cog):  # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot: discord.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Warning System Online")
        self.warn_loop.start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message or not message.guild:
            return
        with open("warns.json", "r") as f:
            warns = json.load(f)
        if not str(message.guild.id) in warns:
            warns[str(message.guild.id)] = {
                str(message.author.id): {}
            }
        elif not str(message.author.id) in warns[str(message.guild.id)]:
            warns[str(message.guild.id)][str(message.author.id)] = {}
        with open("warns.json", "w") as f:
            json.dump(warns, f, indent=4)

    ws = discord.SlashCommandGroup(name="warnings", description="Commands relating to the warning system")

    @ws.command(name="add", description="Adds a warning to a member")
    @has_permissions(kick_members=True)
    async def warn_add(self, ctx: discord.ApplicationContext, member: discord.Member, reason):
        with open("warns.json", "r") as f:
            warns = json.load(f)
        with open("pwarn.json", "r") as f:
            perm = json.load(f)
        if not str(ctx.guild.id) in warns:
            warns[str(ctx.guild.id)] = {
                str(member.id): {}
            }
        elif not str(member.id) in warns[str(ctx.guild.id)]:
            warns[str(ctx.guild.id)][str(member.id)] = {}
        if not str(ctx.guild.id) in perm:
            perm[str(ctx.guild.id)] = {
                str(member.id): []
            }
        elif not str(member.id) in perm[str(ctx.guild.id)]:
            perm[str(ctx.guild.id)][str(member.id)] = []
        num = get_id(member, warns)
        now = datetime.datetime.utcnow()
        nowt = now.timestamp()
        next = timeparse("30d")
        #print(next)
        exp = next + nowt
        warns[str(ctx.guild.id)][str(member.id)][num] = {
            "by": str(ctx.author.id),
            "reason": reason,
            "at": nowt,
            "exp": exp
        }
        perm[str(ctx.guild.id)][str(member.id)].append = {
            "id": str(num),
            "by": str(ctx.author.id),
            "reason": reason,
            "at": nowt,
            "exp": exp
        }
        await warn_check(bot=self.bot, guild=str(member.guild.id), member=str(member.id), warns=warns)
        with open("warns.json", "w") as f:
            json.dump(warns, f, indent=4)
        with open("pwarn.json", "w") as f:
            json.dump(perm, f, indent=4)
        emb = discord.Embed(title="Warn", description=f"**ID: {num}**\n**Offender: {member}**", color=discord.Color.embed_background())
        emb.add_field(name="Reason", value=reason, inline=False)
        emb.timestamp = datetime.datetime.now()
        emb.set_footer(text=f"Added by {ctx.author}")
        with open("channels.json", "r") as f:
            chans = json.load(f)
        if "log" in chans[str(ctx.guild.id)] and int(chans[str(ctx.guild.id)]["log"]) != 0:
            try:
                chan = self.bot.get_channel(int(int(chans[str(ctx.guild.id)]["log"])))
                await chan.send(embed=emb)
            except:
                pass
        await ctx.respond(embed=emb)

    @ws.command(name="remove", description="Removes a warning from a member")
    @has_permissions(kick_members=True)
    async def warn_del(self, ctx: discord.ApplicationContext, member: discord.Member,
                       idd: discord.Option(int, name="id", autocomplete=discord.utils.basic_autocomplete(find_id))):
        with open("warns.json", "r") as f:
            warns = json.load(f)
        with open("warn.json", "r") as f:
            warn = json.load(f)
        if not str(ctx.guild.id) in warns:
            warns[str(ctx.guild.id)] = {
                str(member.id): {}
            }
        elif not str(member.id) in warns[str(ctx.guild.id)]:
            warns[str(ctx.guild.id)][str(member.id)] = {}
        if str(idd) in warns[str(ctx.guild.id)][str(member.id)]:
            emb = discord.Embed(title="Removed Warn", description=f"**ID: {idd}**", color=discord.Color.red())
            usrd = int(warns[str(ctx.guild.id)][str(member.id)][str(idd)]["by"])
            reason = str(warns[str(ctx.guild.id)][str(member.id)][str(idd)]["reason"])
            at = datetime.datetime.utcfromtimestamp(int(warns[str(ctx.guild.id)][str(member.id)][str(idd)]["at"]))
            exp = datetime.datetime.utcfromtimestamp(int(warns[str(ctx.guild.id)][str(member.id)][str(idd)]["exp"]))
            usr = self.bot.get_user(usrd)
            emb.add_field(name="Warned by", value=f"{usr}", inline=False)
            emb.add_field(name="Reason", value=reason, inline=False)
            emb.add_field(name="Warned at", value=f"{at} UTC", inline=False)
            emb.add_field(name="Expires", value=f"{exp} UTC", inline=False)
            emb.timestamp = datetime.datetime.now()
            emb.set_footer(text=f"Removed by {ctx.author}")
            warns[str(ctx.guild.id)][str(member.id)].pop(str(idd))
            num = len(warns[str(ctx.guild.id)][str(member.id)])
            warn[str(ctx.guild.id)][str(member.id)] = num
            with open("warn.json", "w") as f:
                json.dump(warn, f, indent=4)
            with open("warns.json", "w") as f:
                json.dump(warns, f, indent=4)
            with open("channels.json", "r") as f:
                chans = json.load(f)
            if "log" in chans[str(ctx.guild.id)] and int(chans[str(ctx.guild.id)]["log"]) != 0:
                try:
                    chan = self.bot.get_channel(int(int(chans[str(ctx.guild.id)]["log"])))
                    await chan.send(embed=emb)
                except:
                    pass
            await ctx.respond(embed=emb)
        else:
            await ctx.respond(f"**ID: {idd} not found in {member}**")

    @ws.command(name="list", description="Lists a member's warnings")
    async def warn_lst(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open("warns.json", "r") as f:
            warns = json.load(f)
        if not str(ctx.guild.id) in warns:
            warns[str(ctx.guild.id)] = {
                str(member.id): {}
            }
        elif not str(member.id) in warns[str(ctx.guild.id)]:
            warns[str(ctx.guild.id)][str(member.id)] = {}
        emb = discord.Embed(title=f"{member}'s Warnings", color=discord.Color.embed_background())
        for i, v in warns[str(ctx.guild.id)][str(member.id)].items():
            usrd = int(v["by"])
            reason = str(v["reason"])
            at = datetime.datetime.utcfromtimestamp(int(v["at"]))
            exp = datetime.datetime.utcfromtimestamp(int(v["exp"]))
            usr = self.bot.get_user(usrd)
            emb.add_field(name=f"ID: {i}", value=f"- **Warned by:** {usr}\n- **Reason:** {reason}\n- **Warned at:** {at} UTC\n- **Expires:** {exp} UTC", inline=False)
        emb.timestamp = datetime.datetime.now()
        await ctx.respond(embed=emb)

    @ws.command(name="settings", description="Sets warning settings, e.g. 1 warning = 24h mute")
    @has_permissions(administrator=True)
    async def warn_set(self, ctx: discord.ApplicationContext, setting: discord.Option(str, name="setting", description="None: no action, .m: timeout, .k: kick, .b ban. e.g. 1:none,2:.m24h,3:.k,4:.b30d,5:.bF")):
        sets = setting.lower().split(",")
        with open("warnsets.json", "r") as f:
            setts = json.load(f)
        emb = discord.Embed(title="Warning Settings", color=discord.Color.embed_background())
        if str(ctx.guild.id) in setts:
            pass
        else:
            setts[str(ctx.guild.id)] = {}
        for i in sets:
            v = i.split(":")
            setts[str(ctx.guild.id)][str(v[0])] = v[1]
        with open("warnsets.json", "w") as f:
            json.dump(setts, f, indent=4)
        for x, c in setts[str(ctx.guild.id)].items():
            val = ""
            if c == "none":
                val = "nothing"
            elif c.startswith(".m"):
                val = c.removeprefix(".m") + " mute"
            elif c.startswith(".k"):
                val = "kick"
            elif c.startswith(".b"):
                tmp = c.removeprefix(".b")
                if tmp.lower() == "f":
                    val = "Permanent Ban"
                else:
                    val = c.removeprefix(".b") + " ban"
            emb.add_field(name=f"{x} Warnings", value=val, inline=False)
        with open("channels.json", "r") as f:
            chans = json.load(f)
        if "log" in chans[str(ctx.guild.id)] and int(chans[str(ctx.guild.id)]["log"]) != 0:
            try:
                chan = self.bot.get_channel(int(int(chans[str(ctx.guild.id)]["log"])))
                await chan.send(embed=emb)
            except:
                pass
        await ctx.respond(embed=emb)

    @ws.command(name="punishments", description="Punishments for being warned")
    async def ws_puns(self, ctx: discord.ApplicationContext):
        with open("warnsets.json", "r") as f:
            setts = json.load(f)
        emb = discord.Embed(title="Warning Settings", color=discord.Color.embed_background())
        for x, c in setts[str(ctx.guild.id)].items():
            val = ""
            if c == "none":
                val = "nothing"
            elif c.startswith(".m"):
                val = c.removeprefix(".m") + " mute"
            elif c.startswith(".k"):
                val = "kick"
            elif c.startswith(".b"):
                tmp = c.removeprefix(".b")
                if tmp.lower() == "f":
                    val = "Permanent Ban"
                else:
                    val = c.removeprefix(".b") + " ban"
            emb.add_field(name=f"{x} Warnings", value=val, inline=False)
        await ctx.respond(embed=emb)

    @tasks.loop(minutes=1)
    async def warn_loop(self):
        with open("warns.json", "r") as f:
            warns = json.load(f)
        now = datetime.datetime.utcnow().timestamp()
        to = []
        for i in warns:
            #print(i)
            for v in warns[i]:
                #print(v)
                for z, x in warns[i][v].items():
                    #print(z)
                    #print(now)
                    #print(int(x["exp"]))
                    if now >= int(x["exp"]):
                        to.append(f"{i}:{v}:{z}")
                    with open("bans.json", "r") as f:
                        bans = json.load(f)
                    if not i in bans:
                        bans[i] = {}
                        with open("bans.json", "w") as f:
                            json.dump(bans, f, indent=4)
                    if v in bans[i]:
                        if now >= int(bans[i][v]):
                            try:
                                bans[i].pop(v)
                                gld = self.bot.get_guild(i)
                                mem = discord.utils.get(gld.members, id=v)
                                await mem.unban(reason="Ban expired")
                                with open("bans.json", "w") as f:
                                    json.dump(bans, f, indent=4)
                            except:
                                pass

        for i in to:
            v = i.split(":")
            warns[v[0]][v[1]].pop(v[2])
        for i in warns:
            for v in warns[i]:
                await warn_check(bot=self.bot, guild=i, member=v, warns=warns)
        with open("warns.json", "w") as f:
            json.dump(warns, f, indent=4)

def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Warn_System(bot))  # add the cog to the bot

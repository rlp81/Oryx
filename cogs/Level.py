import discord
from discord.ext import commands
import json
from easy_pil import Editor, Canvas, load_image_async, Font
from discord.ext import tasks

defcolr = "#fff0ab"
defmem = {
    "back": "#141414",
    "right": "#fff0ab",
    "bar": "#fff0ab",
    "back_bar": "#000000",
    "font": "poppins",
    "font_color": "#FFFFFF",
    "underline": "#FFFFFF",
    "keeproles": True,
    "getexp": True
}
defset = {
    "next": "lvl:/:0.01",
    "exp": 5,
    "voice": 60,
    "invite": 100,
    "mems": {},
    "roles": {}
}
exm = {
    "898697869580730429": {
        "614257135097872410": {
            "level": 60,
            "exp": 1000
        }
    }
}


def find_invite(invite_list, code):
    for inv in invite_list:
        if inv.code == code:
            return inv
    return False


async def add_roles(bot, guild, user, level):
    with open("lvlset.json", "r") as f:
        set = json.load(f)
    if not guild in set:
        set[guild] = defset
        set[guild]["mems"][user] = defmem
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
    elif not user in set[guild]["mems"]:
        set[guild]["mems"][user] = defmem
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
    add = []
    rem = []
    for i, v in set[guild]["roles"].items():
        if int(level) >= int(i):
            add.append(int(v))
            rem.append(int(v))
    gld = bot.get_guild(int(guild))
    member = await gld.fetch_member(int(user))
    for i in member.roles:
        v = int(i.id)
        if v in add:
            add.remove(v)
    rem.reverse()
    if len(rem) > 0:
        rem.pop(0)
    if bool(set[guild]["mems"][user]["keeproles"]) is False:
        for i in add:
            if not i in rem:
                role = gld.get_role(int(i))
                await member.add_roles(role)
        for i in rem:
            role = gld.get_role(int(i))
            await member.remove_roles(role)
    else:
        for i in add:
            role = gld.get_role(int(i))
            await member.add_roles(role)

async def get_options(ctx: discord.AutocompleteContext):
    item_list = []
    for i, v in defmem.items():
        if i != "getexp":
            item_list.append(i)
    items = []
    for item in item_list:
        value_lower, item_lower = str(ctx.value).lower(), str(item).lower()
        if value_lower in item_lower or ctx.value == '':
            items.append(item)
    return [value for value in items]

def get_next(guild, user, lvl):
    with open("lvlset.json", "r") as f:
        set = json.load(f)
    if not guild in set:
        set[guild] = defset
        set[guild]["mems"][user] = defmem
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
    elif not user in set[guild]["mems"]:
        set[guild]["mems"][user] = defmem
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)

    setng = set[guild]["next"].replace("lvl", str(int(lvl[guild][user]["level"])+1))
    setts = setng.split(":")
    give = int(set[guild]["exp"])
    setts[0] = float(setts[0])
    setts[2] = float(setts[2])
    nxtlvl = 0
    if setts[1] == "/":
        nxtlvl = round(setts[0]/setts[2])
    elif setts[1] == "*":
        nxtlvl = round(setts[0]*setts[2])
    elif setts[1] == "+":
        nxtlvl = round(setts[0]+setts[2])
    elif setts[1] == "-":
        nxtlvl = round(setts[0]-setts[2])
    elif setts[1] == "**":
        nxtlvl = round(setts[0]**setts[2])
    return nxtlvl, give

def get_invite_next(guild, user, lvl):
    with open("lvlset.json", "r") as f:
        set = json.load(f)
    if not guild in set:
        set[guild] = defset
        set[guild]["mems"][user] = defmem
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
    elif not user in set[guild]["mems"]:
        set[guild]["mems"][user] = defmem
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
    elif not "invite" in set[guild]:
        set[guild]["invite"] = "100"

    setng = set[guild]["next"].replace("lvl", str(int(lvl[guild][user]["level"])+1))
    setts = setng.split(":")
    give = int(set[guild]["invite"])
    setts[0] = float(setts[0])
    setts[2] = float(setts[2])
    nxtlvl = 0
    if setts[1] == "/":
        nxtlvl = round(setts[0]/setts[2])
    elif setts[1] == "*":
        nxtlvl = round(setts[0]*setts[2])
    elif setts[1] == "+":
        nxtlvl = round(setts[0]+setts[2])
    elif setts[1] == "-":
        nxtlvl = round(setts[0]-setts[2])
    elif setts[1] == "**":
        nxtlvl = round(setts[0]**setts[2])
    return nxtlvl, give

def get_voice_next(guild, user, lvl):
    with open("lvlset.json", "r") as f:
        set = json.load(f)
    if not guild in set:
        set[guild] = defset
        set[guild]["mems"][user] = defmem
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
    elif not user in set[guild]["mems"]:
        set[guild]["mems"][user] = defmem
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
    elif not "voice" in set[guild]:
        set[guild]["voice"] = 60
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)

    setng = set[guild]["next"].replace("lvl", str(int(lvl[guild][user]["level"])+1))
    setts = setng.split(":")
    give = int(set[guild]["voice"])
    setts[0] = float(setts[0])
    setts[2] = float(setts[2])
    nxtlvl = 0
    if setts[1] == "/":
        nxtlvl = round(setts[0]/setts[2])
    elif setts[1] == "*":
        nxtlvl = round(setts[0]*setts[2])
    elif setts[1] == "+":
        nxtlvl = round(setts[0]+setts[2])
    elif setts[1] == "-":
        nxtlvl = round(setts[0]-setts[2])
    elif setts[1] == "**":
        nxtlvl = round(setts[0]**setts[2])
    return nxtlvl, give


async def add_exp(guild, user, lvl):
    with open("lvlset.json", "r") as f:
        set = json.load(f)
    sett = bool(set[guild]["mems"][user]["getexp"])
    if sett is True:
        nxtlvl, give = get_next(guild, user, lvl)
        lvl[guild][user]["exp"] = int(lvl[guild][user]["exp"]) + give
        if int(lvl[guild][user]["exp"]) >= nxtlvl:
            lvl[guild][user]["exp"] = int(lvl[guild][user]["exp"]) - nxtlvl
            lvl[guild][user]["level"] = int(lvl[guild][user]["level"]) + 1
        with open("level.json", "w") as f:
            json.dump(lvl, f, indent=4)


async def add_invite_exp(guild, user, lvl):
    with open("lvlset.json", "r") as f:
        set = json.load(f)
    sett = bool(set[guild]["mems"][user]["getexp"])
    if sett is True:
        nxtlvl, give = get_invite_next(guild, user, lvl)
        lvl[guild][user]["exp"] = int(lvl[guild][user]["exp"]) + give
        if int(lvl[guild][user]["exp"]) >= nxtlvl:
            lvl[guild][user]["exp"] = int(lvl[guild][user]["exp"]) - nxtlvl
            lvl[guild][user]["level"] = int(lvl[guild][user]["level"]) + 1
        with open("level.json", "w") as f:
            json.dump(lvl, f, indent=4)


async def add_voice_exp(guild, user, time):
    with open("lvlset.json", "r") as f:
        set = json.load(f)
    sett = bool(set[guild]["mems"][user]["getexp"])
    if sett is True:
        with open("level.json", "r") as f:
            lvl = json.load(f)
        nxtlvl, give = get_voice_next(guild, user, lvl)
        total = round(time/give)
        lvl[guild][user]["exp"] = int(lvl[guild][user]["exp"]) + total
        if int(lvl[guild][user]["exp"]) >= nxtlvl:
            lvl[guild][user]["exp"] = int(lvl[guild][user]["exp"]) - nxtlvl
            lvl[guild][user]["level"] = int(lvl[guild][user]["level"]) + 1
        with open("level.json", "w") as f:
            json.dump(lvl, f, indent=4)


class Level(commands.Cog):

    def __init__(self, bot):
        self.bot: discord.Bot = bot
        self.voice = {}
        self.invites = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("Level System Online")
        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except:
                pass
        self.voice_loop.start()

    @tasks.loop(seconds=15)
    async def voice_loop(self):
        add = []
        rem = []
        for i in self.bot.guilds:
            found = []
            if not i.id in self.voice:
                self.voice[i.id] = {}
            for channel in i.voice_channels:
                for v in channel.members:
                    found.append(v.id)
                    if not v.id in self.voice[i.id]:
                        self.voice[i.id][v.id] = {
                            "session": v.voice.session_id,
                            "time": 0,
                        }
                    else:
                        if not v.voice.afk:
                            self.voice[i.id][v.id]["time"] += 15
                    if v.voice.session_id != self.voice[i.id][v.id]["session"] or v.voice.afk is True:
                        tim = self.voice[i.id][v.id]["time"]
                        if tim != 0:
                            self.voice[i.id][v.id]["time"] = 0
                            add.append([i.id, v.id, tim])
                    self.voice[i.id][v.id]["session"] = v.voice.session_id
                    if int(self.voice[i.id][v.id]["time"]) >= 60:
                        self.voice[i.id][v.id]["time"] -= 60
                        add.append([i.id, v.id, 60])
            for usr, stf in self.voice[i.id].items():
                if not usr in found:
                    tim = self.voice[i.id][usr]["time"]
                    if tim != 0:
                        rem.append([i.id, usr])
                        add.append([i.id, usr, tim])
            for r in rem:
                if r[1] in self.voice[r[0]]:
                    self.voice[r[0]].pop(r[1])
        for i in add:
            await add_voice_exp(str(i[0]), str(i[1]), i[2])





    lvlcmd = discord.SlashCommandGroup("levels", description="Commands related to the leveling system")

    setcmd = lvlcmd.create_subgroup(name="set", description="Commands relating to setting values for the leveling system")

    addcmd = lvlcmd.create_subgroup(name="add", description="Commands relating to adding values to the leveling system")

    sercmd = lvlcmd.create_subgroup(name="server", description="Commands relating to leveling system server settings")

    @sercmd.command(name="formula", description="Formula for calculating the exp needed for the next level e.g. lvl/0.01")
    @commands.has_permissions(manage_roles=True)
    async def formula(self, ctx: discord.ApplicationContext, first: str, operator: str, second: str):
        ops = ["+","-","/","*","**"]
        if not operator in ops:
            await ctx.respond("Not a valid operation")
            return
        if not "lvl" in first and not "lvl" in second:
            await ctx.respond("Must mention lvl")
            return
        form = f"{first}:{operator}:{second}"
        with open("lvlset.json", "r") as f:
            set = json.load(f)
        prev = set[str(ctx.guild.id)]["next"]
        set[str(ctx.guild.id)]["next"] = form
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
        await ctx.respond(f"Formula changed from {prev.replace(':', '')} to {form.replace(':', '')}")

    @sercmd.command(name="exp",
                    description="Set the amount of exp every message yields")
    @commands.has_permissions(manage_roles=True)
    async def ser_exp(self, ctx: discord.ApplicationContext, amount: int):
        with open("lvlset.json", "r") as f:
            set = json.load(f)
        prev = set[str(ctx.guild.id)]["exp"]
        set[str(ctx.guild.id)]["exp"] = str(amount)
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
        await ctx.respond(f"Amount of exp for every message changed from {prev} to {amount}.")

    @sercmd.command(name="voice_exp",
                    description="Set the amount of exp every minute in vc yields")
    @commands.has_permissions(manage_roles=True)
    async def ser_exp(self, ctx: discord.ApplicationContext, amount: int):
        with open("lvlset.json", "r") as f:
            set = json.load(f)
        prev = int(set[str(ctx.guild.id)]["exp"])/60
        set[str(ctx.guild.id)]["exp"] = str(60/int(amount))
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
        await ctx.respond(f"Amount of exp for every vc minute changed from {prev} to {amount}.")

    @setcmd.command(name="exp", description="Sets a member's experience")
    @commands.has_permissions(manage_roles=True)
    async def set_exp(self, ctx: discord.ApplicationContext, amount: int, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open("level.json", "r") as f:
            lvl = json.load(f)
        if not str(ctx.guild.id) in lvl:
            lvl[str(ctx.guild.id)] = {
                str(member.id): {
                    "level": 0,
                    "exp": 0
                }
            }
        elif not str(member.id) in lvl[str(ctx.guild.id)]:
            lvl[str(ctx.guild.id)][str(member.id)] = {
                "level": 0,
                "exp": 0
            }
        lvl[str(ctx.guild.id)][str(member.id)]["exp"] = amount

        await ctx.respond(f"Set {member.mention}'s exp to {amount}")
        with open("level.json", "w") as f:
            json.dump(lvl, f, indent=4)

    @addcmd.command(name="exp", description="Adds experience to a member")
    @commands.has_permissions(manage_roles=True)
    async def add_exp(self, ctx: discord.ApplicationContext, amount: int, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open("level.json", "r") as f:
            lvl = json.load(f)
        if not str(ctx.guild.id) in lvl:
            lvl[str(ctx.guild.id)] = {
                str(member.id): {
                    "level": 0,
                    "exp": 0
                }
            }
        elif not str(member.id) in lvl[str(ctx.guild.id)]:
            lvl[str(ctx.guild.id)][str(member.id)] = {
                "level": 0,
                "exp": 0
            }
        lvl[str(ctx.guild.id)][str(member.id)]["exp"] = int(lvl[str(ctx.guild.id)][str(member.id)]["exp"]) + amount

        await ctx.respond(f"Added {amount}xp to {member.mention}")
        with open("level.json", "w") as f:
            json.dump(lvl, f, indent=4)

    @addcmd.command(name="level", description="Adds levels to a member")
    @commands.has_permissions(manage_roles=True)
    async def add_level(self, ctx: discord.ApplicationContext, amount: int, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open("level.json", "r") as f:
            lvl = json.load(f)
        if not str(ctx.guild.id) in lvl:
            lvl[str(ctx.guild.id)] = {
                str(member.id): {
                    "level": 0,
                    "exp": 0
                }
            }
        elif not str(member.id) in lvl[str(ctx.guild.id)]:
            lvl[str(ctx.guild.id)][str(member.id)] = {
                "level": 0,
                "exp": 0
            }
        lvl[str(ctx.guild.id)][str(member.id)]["level"] = int(lvl[str(ctx.guild.id)][str(member.id)]["level"]) + amount

        await ctx.respond(f"Added {amount} levels to {member.mention}")
        with open("level.json", "w") as f:
            json.dump(lvl, f, indent=4)

    @setcmd.command(name="level", description="Sets a member's experience")
    @commands.has_permissions(manage_roles=True)
    async def set_level(self, ctx: discord.ApplicationContext, amount: int, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open("level.json", "r") as f:
            lvl = json.load(f)
        if not str(ctx.guild.id) in lvl:
            lvl[str(ctx.guild.id)] = {
                str(member.id): {
                    "level": 0,
                    "exp": 0
                }
            }
        elif not str(member.id) in lvl[str(ctx.guild.id)]:
            lvl[str(ctx.guild.id)][str(member.id)] = {
                "level": 0,
                "exp": 0
            }
        lvl[str(ctx.guild.id)][str(member.id)]["level"] = amount

        await ctx.respond(f"Set {member.mention}'s level to {amount}")
        with open("level.json", "w") as f:
            json.dump(lvl, f, indent=4)

    @lvlcmd.command(name="rewards", description="Shows rewards for meeting levels")
    async def rewards(self, ctx: discord.ApplicationContext):
        with open("lvlset.json", "r") as f:
            set = json.load(f)
        guild = str(ctx.guild.id)
        emb = discord.Embed(title="Rewards")
        for i, v in set[guild]["roles"].items():
            emb.add_field(name=f"Level {i}", value=ctx.guild.get_role(int(v)).name, inline=False)
        await ctx.respond(embed=emb)

    @lvlcmd.command(name="set_reward", description="Set the reward for meeting a level")
    async def rewards(self, ctx: discord.ApplicationContext, level: int, role: discord.Role):
        with open("lvlset.json", "r") as f:
            set = json.load(f)
        guild = str(ctx.guild.id)
        set[guild]["roles"][str(level)] = str(role.id)
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
        emb = discord.Embed(title="Rewards")
        for i, v in set[guild]["roles"].items():
            role = ctx.guild.get_role(int(v)).name
            emb.add_field(name=str(i), value=role, inline=False)
        await ctx.respond(embed=emb)

    @lvlcmd.command(name="leaderboard", description="Displays the most active users in the server")
    async def leaderboard(self, ctx: discord.ApplicationContext):
        with open("level.json", "r") as f:
            lvl = json.load(f)
        all = []
        lb = []
        top = ""
        for i, v in lvl[str(ctx.guild.id)].items():
            tmp = {
                i: v
            }
            all.append(tmp)
        for x in range(10):
            for i in all:
                for c, v in i.items():
                    if not c in lb:
                        if top == "":
                            top = c
                        else:
                            if int(v["level"]) > int(lvl[str(ctx.guild.id)][top]["level"]):
                                top = c
                            elif int(v["level"]) == int(lvl[str(ctx.guild.id)][top]["level"]):
                                if int(v["exp"]) > int(lvl[str(ctx.guild.id)][top]["exp"]):
                                    top = c
                                elif int(v["exp"]) == int(lvl[str(ctx.guild.id)][top]["exp"]):
                                    top = c
            lb.append(top)
            top = ""
        #lb.reverse()
        emb = discord.Embed(title="Leaderboard")
        num = 0
        for i in lb:
            num += 1
            member = self.bot.get_user(int(i))
            emb.add_field(name=f"{num}. {member}", value=f"Level: {lvl[str(ctx.guild.id)][i]['level']}\nExp: {lvl[str(ctx.guild.id)][i]['exp']}", inline=False)
        await ctx.respond(embed=emb)

    @lvlcmd.command(name="level", description="Returns yours or a specified person's level")
    async def level(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        if member is None:
            member = ctx.author
        with open("level.json", "r") as f:
            lvl = json.load(f)
        with open("lvlset.json", "r") as f:
            set = json.load(f)
        guild = str(ctx.guild.id)
        user = str(ctx.author.id)
        if not guild in set:
            set[guild] = defset
            set[guild]["mems"][user] = defmem
        elif not user in set[guild]["mems"]:
            set[guild]["mems"][user] = defmem
        back = set[guild]["mems"][user]["back"]
        right = set[guild]["mems"][user]["right"]
        back_bar = set[guild]["mems"][user]["back_bar"]
        bar = set[guild]["mems"][user]["bar"]
        fcolor = set[guild]["mems"][user]["font_color"]
        underline = set[guild]["mems"][user]["underline"]
        if member.bot:
            pass
        if not str(member.guild.id) in lvl:
            lvl[str(member.guild.id)] = {
                str(member.id): {
                    "level": 0,
                    "exp": 0
                }
            }
            if not str(member.id) in lvl[str(member.guild.id)]:
                lvl[str(member.guild.id)] = {
                    str(member.id): {
                        "level": 0,
                        "exp": 0
                    }
                }
        exp = lvl[str(member.guild.id)][str(member.id)]["exp"]
        level = lvl[str(member.guild.id)][str(member.id)]["level"]
        nxtlvl, give = get_next(str(member.guild.id), str(member.id), lvl)
        percent = round(int(exp)/int(nxtlvl)*100)
        with open("level.json", "w") as f:
            json.dump(lvl, f, indent=4)
        background = Editor(Canvas((900, 300), color=back))
        prof_pict = await load_image_async(str(member.avatar.url))
        #bot_pict = await load_image_async(str(self.bot.user.avatar.url))
        profile = Editor(prof_pict).resize((150, 150)).circle_image()
        #bot_profile = Editor(bot_pict).resize((150, 150))
        #xy = [(600, 0), (750, 300), (900, 300), (900, 0)]
        #mask = Image.new("L", bot_pict.size, 0)
        #draw = ImageDraw.Draw(mask)
        #draw.polygon(xy, fill=255, outline=None)
        #black = Image.new("L", bot_pict.size, 0)
        #result = Image.composite(bot_pict, black, mask)
        poppins = Font.poppins(size=40)
        poppins_sml = Font.poppins(size=30)
        card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]
        background.polygon(card_right_shape, color=right) #blue: #a4e9e8 Yellow: #ffca53
        #background.paste(result, (600, 0))
        background.paste(profile, (30, 30))
        background.bar((30, 220), max_width=650, height=40, percentage=100, color=back_bar, radius=20)
        background.bar((30, 220), max_width=650, height=40, percentage=percent, color=bar, radius=20)
        background.text((200, 40), f"{member}", font=poppins, color=fcolor)
        background.rectangle((200, 100), width=350, height=2, fill=underline)
        background.text((200, 130), f"Level - {level} | XP - {exp}/{nxtlvl}", font=poppins_sml, color=fcolor)
        await ctx.respond(file=discord.File(fp=background.image_bytes, filename="level_card.png"))

    @lvlcmd.command(name="leveling", description="Configure a user's leveling")
    @commands.has_permissions(manage_channels=True)
    async def lvling(self, ctx: discord.ApplicationContext, member: discord.Member = None, setting: bool = None):
        with open("lvlset.json", "r") as f:
            set = json.load(f)
        guild = str(ctx.guild.id)
        if member is None:
            member = ctx.author
        user = str(member.id)
        if not guild in set:
            set[guild] = defset
            set[guild]["mems"][user] = defmem
        elif not user in set[guild]["mems"]:
            set[guild]["mems"][user] = defmem
        prev = bool(set[guild]["mems"][user]["getexp"])
        if setting is None:
            if prev == True:
                setting = False
            else:
                setting = True
        set[guild]["mems"][user]["getexp"] = setting
        await ctx.respond(f"Set {member.mention}'s leveling to {setting}")



    @lvlcmd.command(name="card", description="Customize your level card!")
    async def card(self, ctx: discord.ApplicationContext,
                   part: discord.Option(str, name="part", description="Specific part to change the color of",
                                        autocomplete=discord.utils.basic_autocomplete(get_options)),
                   setting: discord.Option(str, name="setting", description=f"Setting e.g. font_color {defcolr} or keeproles True")):
        if not part in ["font", "keeproles"]:
            if not setting.startswith("#"):
                setting = "#" + setting
            num = len(setting)
            if num != 7:
                await ctx.respond("Error: Incorrect color value", ephemeral=True)
                return
            else:
                with open("level.json", "r") as f:
                    lvl = json.load(f)
                with open("lvlset.json", "r") as f:
                    set = json.load(f)
                guild = str(ctx.guild.id)
                user = str(ctx.author.id)
                if not guild in set:
                    set[guild] = defset
                    set[guild]["mems"][user] = defmem
                elif not user in set[guild]["mems"]:
                    set[guild]["mems"][user] = defmem
                prev = set[guild]["mems"][user][part]
                set[guild]["mems"][user][part] = setting
                with open("lvlset.json", "w") as f:
                    json.dump(set, f, indent=4)
                await ctx.respond(f"Changed part {part} color from {prev} to {setting}!")
        else:
            with open("lvlset.json", "r") as f:
                set = json.load(f)
            guild = str(ctx.guild.id)
            user = str(ctx.author.id)
            if not guild in set:
                set[guild] = defset
                set[guild]["mems"][user] = defmem
            elif not user in set[guild]["mems"]:
                set[guild]["mems"][user] = defmem
            prev = set[guild]["mems"][user][part]
            if part == "keeproles":
                if setting.lower() == "false":
                    set[guild]["mems"][user][part] = False
                else:
                    set[guild]["mems"][user][part] = True
            with open("lvlset.json", "w") as f:
                json.dump(set, f, indent=4)
            await ctx.respond(f"Changed {part} from {prev} to {setting}!")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        with open("level.json", "r") as f:
            lvl = json.load(f)
        with open("lvlset.json", "r") as f:
            set = json.load(f)
        if message.author.bot:
            return
        if not message.id:
            return
        if not message.guild:
            return
        if not str(message.guild.id) in set:
            set[str(message.guild.id)] = defset
        if not str(message.author.id) in set[str(message.guild.id)]["mems"]:
            set[str(message.guild.id)]["mems"][str(message.author.id)] = defmem
        with open("lvlset.json", "w") as f:
            json.dump(set, f, indent=4)
        if str(message.guild.id) in lvl:
            if str(message.author.id) in lvl[str(message.guild.id)]:
                level = int(lvl[str(message.guild.id)][str(message.author.id)]["level"])
                await add_exp(str(message.guild.id), str(message.author.id), lvl)
                await add_roles(self.bot, str(message.guild.id), str(message.author.id), level)
            else:
                lvl[str(message.guild.id)][str(message.author.id)] = {
                    "level": 0,
                    "exp": 0
                }
                level = int(lvl[str(message.guild.id)][str(message.author.id)]["level"])
                await add_exp(str(message.guild.id), str(message.author.id), lvl)
                await add_roles(self.bot, str(message.guild.id), str(message.author.id), level)
        else:
            lvl[str(message.guild.id)] = {
                str(message.author.id): {
                    "level": 0,
                    "exp": 0
                }
            }
            level = int(lvl[str(message.guild.id)][str(message.author.id)]["level"])
            await add_exp(str(message.guild.id), str(message.author.id), lvl)
            await add_roles(self.bot, str(message.guild.id), str(message.author.id), level)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        invites_before_join = self.invites[member.guild.id]
        invites_after_join = await member.guild.invites()
        found = False
        for invite in invites_after_join:
            use = find_invite(invites_before_join, invite.code)
            if use is False or invite.uses < use.uses:
                if found is False:
                    found = True
                    self.invites[member.guild.id] = invites_after_join
                    add = invite.inviter.id
                    guild = str(member.guild.id)
                    with open("lvlset.json", "r") as f:
                        set = json.load(f)
                    with open("level.json", "r") as f:
                        lvl = json.load(f)
                    if not guild in set:
                        set[guild] = defset
                        with open("lvlset.json", "w") as f:
                            json.dump(set, f, indent=4)
                    if not "invite" in set[guild]:
                        set[guild]["invite"] = "100"
                        with open("lvlset.json", "w") as f:
                            json.dump(set, f, indent=4)
                    if str(member.guild.id) in lvl:
                        if str(add) in lvl[str(member.guild.id)]:
                            level = int(lvl[str(member.guild.id)][str(add)]["level"])
                            await add_invite_exp(guild, str(add), lvl)
                            await add_roles(self.bot, str(member.guild.id), str(add), level)
                        else:
                            lvl[str(member.guild.id)][str(add)] = {
                                "level": 0,
                                "exp": 0
                            }
                            level = int(lvl[str(member.guild.id)][str(add)]["level"])
                            await add_invite_exp(guild, str(add), lvl)
                            await add_roles(self.bot, str(member.guild.id), str(add), level)
                    else:
                        lvl[str(member.guild.id)] = {
                            str(add): {
                                "level": 0,
                                "exp": 0
                            }
                        }
                        level = int(lvl[str(member.guild.id)][str(add)]["level"])
                        await add_invite_exp(guild, str(add), lvl)
                        await add_roles(self.bot, str(member.guild.id), str(add), level)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        self.invites[member.guild.id] = await member.guild.invites()


def setup(bot):
    bot.add_cog(Level(bot))

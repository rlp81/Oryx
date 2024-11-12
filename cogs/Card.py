import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import json
import random

admins = []


async def get_cards(ctx: discord.AutocompleteContext):
    kind = ctx.options['kind']
    kin = "plr"
    if kind == "Player":
        kin = "plr"
    elif kind == "Judge":
        kin = "jdg"
    with open("cards.json", "r") as f:
        cards = json.load(f)
    item_list = []
    for i in cards[kin]:
        item_list.append(str(i))
    items = []
    for item in item_list:
        value_lower, item_lower = str(ctx.value).lower(), str(item).lower()
        if value_lower in item_lower or ctx.value == '':
            items.append(item)
    return [value for value in items]


def get_id():
    with open("cad.json", "r") as f:
        cad = json.load(f)
    found = False
    while found is False:
        num = str(random.randint(00000, 99999))
        if not num in cad:
            found = True
            return num


async def check_game(bot: discord.Bot, msg):
    with open("cad.json", "r") as f:
        cad = json.load(f)
    chan = bot.get_channel(int(cad[msg]["chan"]))
    if cad[msg]["status"] == "stop":
        cad.pop(msg)
        with open("cad.json", "w") as f:
            json.dump(cad, f, indent=4)
        return True, chan
    else:
        return False, None


async def pickjudge(bot, msg, picked):
    with open("cad.json", "r") as f:
        cad = json.load(f)
    stat, chan = await check_game(bot, msg)
    if stat is True:
        try:
            await chan.delete()
            return
        except:
            await chan.send("Failed to delete channel")
    players = []
    for i, v in cad[msg]["players"].items():
        cad[msg]["players"][i]["type"] = "plr"
        if cad[msg]["prev"] != i:
            players.append(i)
    jdg = random.choice(players)
    cad[msg]["prev"] = jdg
    cad[msg]["players"][jdg]["type"] = "jdg"
    cad[msg]["players"][jdg]["picked"] = ""
    with open("cad.json", "w") as f:
        json.dump(cad, f, indent=4)
    await judgecard(bot, msg, picked, jdg)


async def judgecard(bot, msg, picked, jdg):
    with open("cad.json", "r") as f:
        cad = json.load(f)
    with open("cards.json", "r") as f:
        cards = json.load(f)
    stat, chn = await check_game(bot, msg)
    if stat is True:
        try:
            await chn.delete()
            return
        except:
            await chn.send("Failed to delete channel")
    found = False
    card = None
    while found is False:
        card = random.choice(cards["jdg"])
        if not card in picked:
            found = True
    picked.append(card)
    chan = bot.get_channel(int(cad[msg]["chan"]))
    jud = await bot.fetch_user(int(jdg))
    embed = discord.Embed(title=f"{jud.name} is the Judge!", description=f"The judge prompt is:\n**{card}**\n# You have 25 seconds to place a card")
    await chan.send(embed=embed)
    await asyncio.sleep(25)
    await getrandomcards(bot, msg, picked, jdg, chan)


async def getrandomcards(bot, msg, picked, jdg, chan):
    with open("cad.json", "r") as f:
        cad = json.load(f)
    stat, chn = await check_game(bot, msg)
    if stat is True:
        try:
            await chn.delete()
            return
        except:
            await chn.send("Failed to delete channel")
    current = []
    for i, v in cad[msg]["players"].items():
        if v["type"] == "plr":
            if v["picked"] == "":
                pick = random.choice(v["hand"])
                cad[msg]["players"][i]["hand"].remove(pick)
                cad[msg]["players"][i]["picked"] = pick
            current.append([cad[msg]["players"][i]["picked"], i])
    cad[msg]["current"] = current
    with open("cad.json", "w") as f:
        json.dump(cad, f, indent=4)
    embed = discord.Embed(title="Selected cards", description="You have 20 seconds to select a card")
    num = 0
    opts = []
    for i in cad[msg]["current"]:
        num += 1
        opts.append(discord.SelectOption(label=str(num)))
        embed.add_field(name=f"{num}", value=i[0], inline=False)
    view = Pick(typ="jdg")
    selc = Sel(opts=opts)
    view.add_item(selc)
    await chan.send(embed=embed, view=view)
    await asyncio.sleep(20)
    await judgerandomcard(bot, msg, picked, jdg, chan)


async def judgerandomcard(bot, msg, picked, jdg, chan):
    with open("cad.json", "r") as f:
        cad = json.load(f)
    stat, chn = await check_game(bot, msg)
    if stat is True:
        try:
            await chn.delete()
            return
        except:
            await chn.send("Failed to delete channel")
    if cad[msg]["players"][jdg]["picked"] == "":
        card = random.randint(1, len(cad[msg]["current"]))
        cad[msg]["players"][jdg]["picked"] = str(card)
    card = cad[msg]["current"][int(cad[msg]["players"][jdg]["picked"])-1]
    cad[msg]["players"][str(card[1])]["points"] = str(int(cad[msg]["players"][str(card[1])]["points"]) + 1)
    with open("cad.json", "w") as f:
        json.dump(cad, f, indent=4)
    jud = await bot.fetch_user(int(jdg))
    win = await bot.fetch_user(int(card[1]))
    embed = discord.Embed(title=f"{jud.name} picked {win.name}'s card!", description=card[0])
    await chan.send(embed=embed)
    await checkwinner(bot, msg, picked, chan)


async def checkwinner(bot, msg, picked, chan):
    with open("cad.json", "r") as f:
        cad = json.load(f)
    stat, chn = await check_game(bot, msg)
    if stat is True:
        try:
            await chn.delete()
            return
        except:
            await chn.send("Failed to delete channel")
    win = None
    for i, v in cad[msg]["players"].items():
        if int(v["points"]) >= 5:
            win = i
            break
    if not win is None:
        winr = await bot.fetch_user(int(win))
        await chan.send(f"{winr.name} has won! The game has ended. Channel deleting in 20 seconds.")
        cad.pop(msg)
        with open("cad.json", "w") as f:
            json.dump(cad, f, indent=4)
        await asyncio.sleep(20)
        try:
            await chan.delete()
        except:
            await chan.send(f"Failed to delete channel")
    else:
        await givecards(bot, msg, picked)


async def givecards(bot, msg, picked):
    with open("cad.json", "r") as f:
        cad = json.load(f)
    stat, chn = await check_game(bot, msg)
    if stat is True:
        try:
            await chn.delete()
            return
        except:
            await chn.send("Failed to delete channel")
    with open("cards.json", "r") as f:
        cards = json.load(f)
    for i, v in cad[msg]["players"].items():
        num = len(v["hand"])
        cad[msg]["players"][i]["picked"] = ""
        if num < 6:
            amt = 6 - num
            for x in range(amt):
                found = False
                while found is False:
                    card = random.choice(cards["plr"])
                    if not card in picked:
                        cad[msg]["players"][i]["hand"].append(card)
                        picked.append(card)
                        found = True
    with open("cad.json", "w") as f:
        json.dump(cad, f, indent=4)
    await pickjudge(bot, msg, picked)


class Sel(discord.ui.Select):

    def __init__(self, opts):
        super().__init__(placeholder="Select a card", options=opts)

    async def callback(self, interaction: discord.Interaction):
        with open("cad.json", "r") as f:
            cad = json.load(f)
        if self.view.typ == "jdg":
            usr = str(interaction.user.id)
            msg = str(interaction.channel.topic)
            number = int(self.values[0])
            if msg:
                if msg in cad:
                    if cad[msg]["players"][usr]["type"] == "jdg":
                        if cad[msg]["current"][number - 1]:
                            cad[msg]["players"][usr]["picked"] = str(number)
                            with open("cad.json", "w") as f:
                                json.dump(cad, f, indent=4)
                            await interaction.response.send_message(f"Picked card {number}", ephemeral=True)
                        else:
                            await interaction.response.send_message("Invalid card", ephemeral=True)
                    else:
                        await interaction.response.send_message("You must be a judge to use this command", ephemeral=True)
                else:
                    await interaction.response.send_message(f"Not a game", ephemeral=True)
            else:
                await interaction.response.send_message(f"Not a game", ephemeral=True)
        elif self.view.typ == "plr":
            usr = str(interaction.user.id)
            msg = str(interaction.channel.topic)
            number = int(self.values[0])
            if msg:
                if msg in cad:
                    if usr in cad[msg]["players"]:
                        if cad[msg]["players"][usr]["type"] == "plr":
                            if cad[msg]["players"][usr]["hand"] != []:
                                if cad[msg]["players"][usr]["picked"] == "":
                                    if cad[msg]["players"][usr]["hand"][number - 1]:
                                        card = cad[msg]["players"][usr]["hand"][number - 1]
                                        cad[msg]["players"][usr]["picked"] = card
                                        cad[msg]["players"][usr]["hand"].remove(card)
                                        with open("cad.json", "w") as f:
                                            json.dump(cad, f, indent=4)
                                        await interaction.response.send_message(f"Picked card: {card}", ephemeral=True)
                                    else:
                                        await interaction.response.send_message(f"No such card", ephemeral=True)
                                else:
                                    await interaction.response.send_message(f"Card already picked", ephemeral=True)
                            else:
                                await interaction.response.send_message(f"Hand empty", ephemeral=True)
                        else:
                            await interaction.response.send_message(f"You must be a player to use this command", ephemeral=True)
                    else:
                        await interaction.response.send_message(f"Not a part of game.", ephemeral=True)
                else:
                    await interaction.response.send_message(f"Not a game", ephemeral=True)
            else:
                await interaction.response.send_message(f"Not a game", ephemeral=True)


class Pick(discord.ui.View):

    def __init__(self, typ):
        super().__init__(timeout=25, disable_on_timeout=True)
        self.typ = typ


class But(discord.ui.Button):

    def __init__(self, lab):
        super().__init__(label=lab)

    async def callback(self, interaction: discord.Interaction):
        with open("cad.json", "r") as f:
            cad = json.load(f)
        if self.view.typ == "jdg":
            usr = str(interaction.user.id)
            msg = str(interaction.channel.topic)
            number = int(self.label)
            if msg:
                if msg in cad:
                    if cad[msg]["players"][usr]["type"] == "jdg":
                        if cad[msg]["current"][number - 1]:
                            cad[msg]["players"][usr]["picked"] = str(number)
                            with open("cad.json", "w") as f:
                                json.dump(cad, f, indent=4)
                            await interaction.response.send_message(f"Picked card {number}", ephemeral=True)
                        else:
                            await interaction.response.send_message("Invalid card", ephemeral=True)
                    else:
                        await interaction.response.send_message("You must be a judge to use this command", ephemeral=True)
                else:
                    await interaction.response.send_message(f"Not a game", ephemeral=True)
            else:
                await interaction.response.send_message(f"Not a game", ephemeral=True)
        elif self.view.typ == "plr":
            usr = str(interaction.user.id)
            msg = str(interaction.channel.topic)
            number = int(self.label)
            if msg:
                if msg in cad:
                    if usr in cad[msg]["players"]:
                        if cad[msg]["players"][usr]["type"] == "plr":
                            if cad[msg]["players"][usr]["hand"] != []:
                                if cad[msg]["players"][usr]["picked"] == "":
                                    if cad[msg]["players"][usr]["hand"][number - 1]:
                                        card = cad[msg]["players"][usr]["hand"][number - 1]
                                        cad[msg]["players"][usr]["picked"] = card
                                        cad[msg]["players"][usr]["hand"].remove(card)
                                        with open("cad.json", "w") as f:
                                            json.dump(cad, f, indent=4)
                                        await interaction.response.send_message(f"Picked card: {card}", ephemeral=True)
                                    else:
                                        await interaction.response.send_message(f"No such card", ephemeral=True)
                                else:
                                    await interaction.response.send_message(f"Card already picked", ephemeral=True)
                            else:
                                await interaction.response.send_message(f"Hand empty", ephemeral=True)
                        else:
                            await interaction.response.send_message(f"You must be a player to use this command", ephemeral=True)
                    else:
                        await interaction.response.send_message(f"Not a part of game.", ephemeral=True)
                else:
                    await interaction.response.send_message(f"Not a game", ephemeral=True)
            else:
                await interaction.response.send_message(f"Not a game", ephemeral=True)


class Join(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Join", style=discord.ButtonStyle.green, custom_id="join")
    async def joincall(self, button: discord.Button, interaction: discord.Interaction):
        with open("cad.json", "r") as f:
            cad = json.load(f)
        if not str(interaction.user.id) in cad[str(interaction.message.id)]["players"]:
            if cad[str(interaction.message.id)]["status"] == "open":
                cad[str(interaction.message.id)]["players"][str(interaction.user.id)] = {
                        "type": "plr",
                        "points": "0",
                        "hand": [],
                        "picked": ""
                    }
                with open("cad.json", "w") as f:
                    json.dump(cad, f, indent=4)
                chan = interaction.guild.get_channel(int(cad[str(interaction.message.id)]["chan"]))
                await interaction.respond("You joined the game!", ephemeral=True)
                await chan.set_permissions(interaction.user, view_channel=True, send_messages=True, read_messages=True,
                                                add_reactions=True,
                                                embed_links=True, attach_files=True, read_message_history=True,
                                                external_emojis=True, use_application_commands=True)
                await chan.send(f"{interaction.user.mention} has joined! Players: {len(cad[str(interaction.message.id)]['players'])}")
            else:
                await interaction.respond("Game already started!", ephemeral=True)
        else:
            await interaction.respond("You are already in the game!", ephemeral=True)

    @discord.ui.button(label="Leave", style=discord.ButtonStyle.red, custom_id="leave")
    async def leavecall(self, button: discord.Button, interaction: discord.Interaction):
        with open("cad.json", "r") as f:
            cad = json.load(f)
        if str(interaction.user.id) in cad[str(interaction.message.id)]["players"]:
            if cad[str(interaction.message.id)]["status"] == "open":
                chan = interaction.guild.get_channel(int(cad[str(interaction.message.id)]["chan"]))
                cad[str(interaction.message.id)]["players"].pop(str(interaction.user.id))
                await interaction.respond("You left the game!", ephemeral=True)
                await chan.send(f"{interaction.user.mention} has left! Players: {len(cad[str(interaction.message.id)]['players'])}")
                await chan.set_permissions(interaction.user, view_channel=False, send_messages=False, read_messages=False,
                                                add_reactions=False,
                                                embed_links=False, attach_files=False, read_message_history=False,
                                                external_emojis=False, use_application_commands=False)
            else:
                await interaction.respond("Game already started!", ephemeral=True)
            with open("cad.json", "w") as f:
                json.dump(cad, f, indent=4)
        else:
            await interaction.respond("You are not in the game!", ephemeral=True)


class StartView(discord.ui.View):

    def __init__(self, bot):
        self.bot: discord.Bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green, custom_id="start")
    async def callback(self, button: discord.Button, interaction: discord.Interaction):
        msg = str(interaction.channel.topic)
        with open("cad.json", "r") as f:
            cad = json.load(f)
        plrs = len(cad[msg]["players"])
        if str(interaction.user.id) == cad[msg]["own"]:
            if plrs >= 3:
                with open("cards.json", "r") as f:
                    cards = json.load(f)
                self.disable_all_items()
                await interaction.response.edit_message(embeds=interaction.message.embeds, view=self)
                message = self.bot.get_message(int(msg))
                if not message is None:
                    view = discord.ui.View.from_message(message)
                    view.disable_all_items()
                    embs = message.embeds
                    await message.edit(embeds=embs, view=view)
                cad[msg]["status"] = "closed"
                picked = []
                for i, v in cad[msg]["players"].items():
                    for x in range(6):
                        found = False
                        while found is False:
                            card = random.choice(cards["plr"])
                            if not card in picked:
                                picked.append(card)
                                cad[msg]["players"][i]["hand"].append(card)
                                found = True
                with open("cad.json", "w") as f:
                    json.dump(cad, f, indent=4)
                await pickjudge(self.bot, msg, picked)



            else:
                await interaction.respond("Not enough players!", ephemeral=True)
        else:
            await interaction.respond("Only the host can start the game!", ephemeral=True)


class Card(commands.Cog):

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cards Against Discord Online")

    cmd = discord.SlashCommandGroup(name="cad", description="Cards against Discord")

    plr = cmd.create_subgroup(name="player", description="Player commands")

    adm = cmd.create_subgroup(name="admin", description="Admin commands", guild_ids=[866127811000401921, 849423106362835014, 898697869580730429])

    @cmd.command(name="set-category", description="Set the CAD Category")
    @has_permissions(manage_channels=True)
    async def set_category(self, ctx: discord.ApplicationContext, category: discord.CategoryChannel):
        guild = ctx.guild
        with open("channels.json", "r") as f:
            chans = json.load(f)
        if not str(guild.id) in chans:
            chans[str(guild.id)] = {}
            chans[str(guild.id)]["welcome"] = 0
            chans[str(guild.id)]["leave"] = 0
            chans[str(guild.id)]["log"] = 0
            chans[str(guild.id)]["yt"] = 0
            chans[str(guild.id)]["cad"] = 0
            chans[str(guild.id)]["black"] = []
            chans[str(guild.id)]["roles"] = []
        chans[str(guild.id)]["cad"] = category.id
        await ctx.respond(f"Set the Cards Against Discord Category to {category.mention}")
        with open("channels.json", "w") as f:
            json.dump(chans, f, indent=4)

    @cmd.command(name="stop", description="Stop a game")
    @has_permissions(manage_channels=True)
    async def set_category(self, ctx: discord.ApplicationContext):
        with open("cad.json", "r") as f:
            cad = json.load(f)
        usr = str(ctx.author.id)
        msg = str(ctx.channel.topic)
        if msg:
            if msg in cad:
                if usr == cad[msg]["own"]:
                    cad[msg]["status"] = "stop"
                    with open("cad.json", "w") as f:
                        json.dump(cad, f, indent=4)
                    await ctx.respond("Stopping game..")
                else:
                    await ctx.respond("Only the host can use this command")
            else:
                await ctx.respond("Not a game")
        else:
            await ctx.respond("Not a game")

    @cmd.command(name="start", description="Starts a game of Cards against Discord")
    async def _start(self, ctx: discord.ApplicationContext):
        with open("cad.json", "r") as f:
            cad = json.load(f)

        num = get_id()
        view = Join()
        embed = discord.Embed(title="Cards Against Discord", description=f"{ctx.author} "
                                                                         f"is hosting a game of Cards Against Discord!")
        await ctx.respond("Generating..", ephemeral=True)
        msg = await ctx.send(embed=embed, view=view)
        with open("channels.json", "r") as f:
            chans = json.load(f)
        guild = ctx.guild
        if not str(guild.id) in chans:
            chans[str(guild.id)] = {}
            chans[str(guild.id)]["welcome"] = 0
            chans[str(guild.id)]["leave"] = 0
            chans[str(guild.id)]["log"] = 0
            chans[str(guild.id)]["yt"] = 0
            chans[str(guild.id)]["cad"] = 0
            chans[str(guild.id)]["black"] = []
            chans[str(guild.id)]["roles"] = []
            with open("channels.json", "w") as f:
                json.dump(chans, f, indent=4)
        cat = int(chans[str(ctx.guild.id)]["cad"])
        if cat != 0:
            chan = await ctx.guild.create_text_channel(category=ctx.guild.get_channel(cat), name=f"cad-{num}",
                                                       topic=f"{msg.id}")
            await chan.set_permissions(ctx.guild.default_role, view_channel=False, send_messages=False, read_messages=False,
                                       add_reactions=False,
                                       embed_links=False, attach_files=False, read_message_history=False,
                                       external_emojis=False, use_application_commands=False)
            await chan.set_permissions(ctx.author, view_channel=True, send_messages=True, read_messages=True,
                                       add_reactions=False,
                                       embed_links=True, attach_files=True, read_message_history=True,
                                       external_emojis=True, use_application_commands=True)
            embed = discord.Embed(title="Start the game!", description="## Commands\n### Player\n- /cad player pick: Pick a card to play")
            view = StartView(self.bot)
            cad[str(msg.id)] = {
                "status": "open",
                "own": str(ctx.author.id),
                "chan": str(chan.id),
                "players": {
                    str(ctx.author.id): {
                        "type": "plr",
                        "points": "0",
                        "hand": [],
                        "picked": ""
                    }
                },
                "current": [],
                "prev": [],
                "id": num
            }
            with open("cad.json", "w") as f:
                json.dump(cad, f, indent=4)
            await chan.send(embed=embed, view=view)

    @plr.command(name="pick", description="Select the card to play")
    async def pick(self, ctx: discord.ApplicationContext):
        with open("cad.json", "r") as f:
            cad = json.load(f)
        usr = str(ctx.author.id)
        msg = str(ctx.channel.topic)
        if msg:
            if msg in cad:
                if usr in cad[msg]["players"]:
                    if cad[msg]["players"][usr]["type"] == "plr":
                        if cad[msg]["players"][usr]["hand"] != []:
                            if cad[msg]["players"][usr]["picked"] == "":
                                emb = discord.Embed(title=f"{ctx.author.name}'s Hand")
                                num = 0
                                view = Pick(typ="plr")
                                opts = []
                                for i in cad[msg]["players"][usr]["hand"]:
                                    num += 1
                                    opts.append(discord.SelectOption(label=str(num)))
                                    emb.add_field(name=str(num), value=i)
                                selc = Sel(opts=opts)
                                view.add_item(selc)
                                await ctx.respond(embed=emb, view=view, ephemeral=True)
                            else:
                                await ctx.respond(f"Card already picked", ephemeral=True)
                        else:
                            await ctx.respond(f"Hand empty", ephemeral=True)
                    else:
                        await ctx.respond(f"You must be a player to use this command", ephemeral=True)
                else:
                    await ctx.respond(f"Not a part of game.", ephemeral=True)
            else:
                await ctx.respond(f"Not a game", ephemeral=True)
        else:
            await ctx.respond(f"Not a game", ephemeral=True)

    @adm.command(name="add", description="Add a card")
    async def add(self, ctx: discord.ApplicationContext, kind: discord.Option(str, name="kind", choices=["Player", "Judge"]), card: str):
        if ctx.author.id in admins:
            kin = "plr"
            if kind == "Player":
                kin = "plr"
            elif kind == "Judge":
                kin = "jdg"
            with open("cards.json", "r") as f:
                cards = json.load(f)
            if not "plr" in cards:
                cards["plr"] = []
            if not "jdg" in cards:
                cards["jdg"] = []
            if not card in cards[kin]:
                cards[kin].append(card)
                emb = discord.Embed(title=f"Added {kind} Card", description=card)
                await ctx.respond(embed=emb)
            else:
                await ctx.respond("Card already exists", ephemeral=True)
            with open("cards.json", "w") as f:
                json.dump(cards, f, indent=4)
        else:
            await ctx.respond("Not authorized", ephemeral=True)

    @adm.command(name="remove", description="Removes a card")
    async def add(self, ctx: discord.ApplicationContext,
                  kind: discord.Option(str, name="kind", choices=["Player", "Judge"]),
                  card: discord.Option(str, name="card", autocomplete=discord.utils.basic_autocomplete(get_cards))):
        if ctx.author.id in admins:
            kin = "plr"
            if kind == "Player":
                kin = "plr"
            elif kind == "Judge":
                kin = "jdg"
            with open("cards.json", "r") as f:
                cards = json.load(f)
            if not "plr" in cards:
                cards["plr"] = []
            if not "jdg" in cards:
                cards["jdg"] = []
            if card in cards[kin]:
                cards[kin].remove(card)
                emb = discord.Embed(title=f"Removed {kind} Card", description=card)
                await ctx.respond(embed=emb)
            else:
                await ctx.respond("Card doesn't exists", ephemeral=True)
            with open("cards.json", "w") as f:
                json.dump(cards, f, indent=4)
        else:
            await ctx.respond("Not authorized", ephemeral=True)


def setup(bot):
    bot.add_cog(Card(bot))

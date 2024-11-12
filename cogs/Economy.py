import datetime
import discord
import json
import random
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, BucketType, cooldown
from discord import option
from pytimeparse.timeparse import timeparse

blackmul = 2.5
cards = [
    ["Hearts", "Spades", "Clubs", "Diamonds"], {"two":[2,2], "three":[3,3], "four":[4,4], "five":[5,5], "six":[6,6], "seven":[7,7], "eight":[8,8], "nine":[9,9], "jack":[10,10], "queen":[10,10], "king":[10,10], "ace":[1,10]}
]


pshops = {
    "axe": {
        "axe": {
            "name": "Axe",
            "price": 8
        },
        "iron": {
            "name": "Iron Axe",
            "price": 25
        },
        "steel": {
            "name": "Steel Axe",
            "price": 40
        }
    },
    "pickaxe": {
            "pickaxe": {
                "name": "Pickaxe",
                "price": 10
            },
            "iron": {
                "name": "Iron Pickaxe",
                "price": 30
            },
            "steel": {
                "name": "Steel Pickaxe",
                "price": 50
            }
        },

}

async def get_items(ctx: discord.AutocompleteContext):
    item_list = []
    with open("inventory.json", "r") as f:
        inv = json.load(f)
    if not str(ctx.interaction.user.id) in inv[str(ctx.interaction.guild_id)]:
        inv[str(ctx.interaction.guild_id)][str(ctx.interaction.user.id)] = {}
        with open("inventory.json", "w") as f:
            json.dump(inv, f, indent=4)
    for i, v in inv[str(ctx.interaction.guild_id)][str(ctx.interaction.user.id)].items():
        item_list.append(i)
    items = []
    for item in item_list:
        value_lower, item_lower = str(ctx.value).lower(), str(item).lower()
        if value_lower in item_lower or ctx.value == '':
            items.append(item)
    return [value for value in items]


async def get_crafts(ctx: discord.AutocompleteContext):
    item_list = []
    with open("items.json", "r") as f:
        itm = json.load(f)
    for i, v in itm.items():
        if isinstance(v["craft"], dict):
            item_list.append(i)
    items = []
    for item in item_list:
        value_lower, item_lower = str(ctx.value).lower(), str(item).lower()
        if value_lower in item_lower or ctx.value == '':
            items.append(item)
    return [value for value in items]


async def get_exps(ctx: discord.AutocompleteContext):
    item_list = []
    with open("items.json", "r") as f:
        itms = json.load(f)
    for i, v in itms.items():
        item_list.append(i)
    items = []
    for item in item_list:
        value_lower, item_lower = str(ctx.value).lower(), str(item).lower()
        if value_lower in item_lower or ctx.value == '':
            items.append(item)
    return [value for value in items]

async def get_blds(ctx: discord.AutocompleteContext):
    item_list = ["inventory", "server"]
    with open("builds.json", "r") as f:
        blds = json.load(f)
    if not str(ctx.interaction.user.id) in blds[str(ctx.interaction.guild_id)]:
        blds[str(ctx.interaction.guild_id)][str(ctx.interaction.user.id)] = {}
        with open("builds.json", "w") as f:
            json.dump(blds, f, indent=4)
    for i, v in blds[str(ctx.interaction.guild_id)][str(ctx.interaction.user.id)].items():
        item_list.append(blds[str(ctx.interaction.guild_id)][str(ctx.interaction.user.id)][i]["name"])
    items = []
    for item in item_list:
        value_lower, item_lower = str(ctx.value).lower(), str(item).lower()
        if value_lower in item_lower or ctx.value == '':
            items.append(item)
    return [value for value in items]

async def get_blds1(ctx: discord.AutocompleteContext):
    item_list = []
    with open("build.json", "r") as f:
        build = json.load(f)
    for i, v in build.items():
        item_list.append(v["name"])
    items = []
    for item in item_list:
        value_lower, item_lower = str(ctx.value).lower(), str(item).lower()
        if value_lower in item_lower or ctx.value == '':
            items.append(item)
    return [value for value in items]

def getshops(guild):
    with open("shops.json", "r") as f:
        shop = json.load(f)
    if str(guild) in shop:
        shops = shop[str(guild)]["shops"]
        options = []
        for i, v in shops.items():
            options.append(
                discord.SelectOption(
                    label=i,
                    description=shop[str(guild)][i]["desc"]
            ))
        return options
    else:
        guild = str(guild)
        shop[guild] = {
            "level": 0,
            "shops": {
                "axe": {
                    "locked": True,
                    "desc": "Axe Shop",
                    "level": 1,
                    "price": 200,
                    "owner": None,
                    "items": {
                        "axe": {
                            "name": "Axe",
                            "price": 8,
                            "level": 1
                        },
                        "iron": {
                            "name": "Iron Axe",
                            "price": 25,
                            "level": 2
                        },
                        "steel": {
                            "name": "Steel Axe",
                            "price": 40,
                            "level": 3
                        }
                    }
                },
                "pickaxe": {
                    "locked": True,
                    "desc": "Pickaxe Shop",
                    "level": 1,
                    "price": 500,
                    "owner": None,
                    "items": {
                        "pickaxe": {
                            "name": "Pickaxe",
                            "price": 10,
                            "level": 1
                        },
                        "iron": {
                            "name": "Iron Pickaxe",
                            "price": 30,
                            "level": 2
                        },
                        "steel": {
                            "name": "Steel Pickaxe",
                            "price": 50,
                            "level": 3
                        }
                    }
                }
            }
        }
        """
        shop[guild]["Server"] = {}
        shop[guild]["Server"]["desc"] = "Server Shop"
        shop[guild]["Server"]["items"] = {}
        shop[guild]["Server"]["money"] = {}
        shop[guild]["Server"]["money"]["total"] = 10000000
        """
        with open("shops.json", "w") as f:
            json.dump(shop, f, indent=4)
        shops = shop[str(guild)]["shops"]
        options = []
        for i, v in shops.items():
            options.append(
                discord.SelectOption(
                    label=i,
                    description=shop[str(guild)][i]["desc"]
            ))
        return options


class blackview(discord.ui.View):

    def __init__(self, used, user, deal, amount):
        self.used = used
        self.user = user
        self.deal = deal
        self.amount = amount
        names = [[], []]
        for i in range(4):
            if i < 2:
                names[0].append(used[i])
            else:
                names[1].append(used[i])
        self.names = names
        super().__init__(timeout=15)

    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(view=self)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.gray)
    async def hit(self, button, interaction: discord.Interaction):
        find = False
        card = None
        bust = 0
        while find is False:
            house = random.randint(0, 3)
            card = random.choice(list(cards[1].keys()))
            name = f"{house}-{card}"
            if not name in self.used:
                self.used.append(name)
                self.names[1].append(name)
                find = True
        num = cards[1][card]
        self.user[0] += num[0]
        self.user[1] += num[1]
        if self.user[0] > 21 or self.user[1] > 21:
            bust = 1
        elif self.user[0] == 21 or self.user[1] == 21:
            bust = -1
        if bust == 0:
            if self.deal[0] < 16 or self.deal[1] < 16:
                find = False
                card = None
                while find is False:
                    house = random.randint(0, 3)
                    card = random.choice(list(cards[1].keys()))
                    name = f"{house}-{card}"
                    if not name in self.used:
                        self.used.append(name)
                        self.names[0].append(name)
                        find = True
                num = cards[1][card]
                self.deal[0] += num[0]
                self.deal[1] += num[1]
                if self.deal[0] > 21 or self.deal[1] > 21:
                    bust = 2
                elif self.deal[0] == 21 or self.deal[1] == 21:
                    bust = -2
        elif bust == -1:
            emb = discord.Embed(title="Blackjack")
            val = ""
            f = True
            for i in self.names[0]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Dealer", value=val, inline=False)
            val = ""
            f = True
            for i in self.names[1]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Player", value=val, inline=False)
            self.disable_all_items()
            await interaction.edit(embed=emb, view=self)
            gain = self.amount*blackmul
            with open("balance.json", "r") as f:
                bal = json.load(f)
            guild = str(interaction.guild_id)
            mem = str(interaction.user.id)
            bal[guild][mem]["wallet"] = int(bal[guild][mem]["wallet"]) + gain
            with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)
            await interaction.message.reply(f"You won! You have won {gain} money!")
        elif bust == 1:
            emb = discord.Embed(title="Blackjack")
            val = ""
            f = True
            for i in self.names[0]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Dealer", value=val, inline=False)
            val = ""
            f = True
            for i in self.names[1]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Player", value=val, inline=False)
            self.disable_all_items()
            await interaction.edit(embed=emb, view=self)
            with open("balance.json", "r") as f:
                bal = json.load(f)
            guild = str(interaction.guild_id)
            mem = str(interaction.user.id)
            bal[guild][mem]["wallet"] = int(bal[guild][mem]["wallet"]) - self.amount
            with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)
            await interaction.message.reply(f"You lost! You have lost {self.amount} money!")
        if bust == 2:
            emb = discord.Embed(title="Blackjack")
            val = ""
            f = True
            for i in self.names[0]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Dealer", value=val, inline=False)
            val = ""
            f = True
            for i in self.names[1]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Player", value=val, inline=False)
            self.disable_all_items()
            await interaction.edit(embed=emb, view=self)
            gain = self.amount * blackmul
            with open("balance.json", "r") as f:
                bal = json.load(f)
            guild = str(interaction.guild_id)
            mem = str(interaction.user.id)
            bal[guild][mem]["wallet"] = int(bal[guild][mem]["wallet"]) + gain
            with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)
            await interaction.message.reply(f"You won! You have won {gain} money!")
        elif bust == -2:
            emb = discord.Embed(title="Blackjack")
            val = ""
            f = True
            for i in self.names[0]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Dealer", value=val, inline=False)
            val = ""
            f = True
            for i in self.names[1]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Player", value=val, inline=False)
            self.disable_all_items()
            await interaction.edit(embed=emb, view=self)
            with open("balance.json", "r") as f:
                bal = json.load(f)
            guild = str(interaction.guild_id)
            mem = str(interaction.user.id)
            bal[guild][mem]["wallet"] = int(bal[guild][mem]["wallet"]) - self.amount
            with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)
            await interaction.message.reply(f"You lost! You have lost {self.amount} money!")
        if bust == 0:
            emb = discord.Embed(title="Blackjack")
            val = ""
            f = True
            for i in self.names[0]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Dealer", value=val, inline=False)
            val = ""
            f = True
            for i in self.names[1]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Player", value=val, inline=False)
            await interaction.edit(embed=emb, view=self)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.gray)
    async def stand(self, button, interaction: discord.Interaction):
        bust = 0
        find = False
        card = None
        while find is False:
            house = random.randint(0, 3)
            card = random.choice(list(cards[1].keys()))
            name = f"{house}-{card}"
            if not name in self.used:
                self.used.append(name)
                self.names[0].append(name)
                find = True
        num = cards[1][card]
        self.deal[0] += num[0]
        self.deal[1] += num[1]
        if self.deal[0] > 21 or self.deal[1] > 21:
            bust = 2
        elif self.deal[0] == 21 or self.deal[1] == 21:
            bust = -2
        if bust == 2:
            emb = discord.Embed(title="Blackjack")
            val = ""
            f = True
            for i in self.names[0]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Dealer", value=val, inline=False)
            val = ""
            f = True
            for i in self.names[1]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Player", value=val, inline=False)
            self.disable_all_items()
            await interaction.edit(embed=emb, view=self)
            gain = self.amount * blackmul
            with open("balance.json", "r") as f:
                bal = json.load(f)
            guild = str(interaction.guild_id)
            mem = str(interaction.user.id)
            bal[guild][mem]["wallet"] = int(bal[guild][mem]["wallet"]) + gain
            with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)
            await interaction.message.reply(f"You won! You have won {gain} money!")
        elif bust == -2:
            emb = discord.Embed(title="Blackjack")
            val = ""
            f = True
            for i in self.names[0]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Dealer", value=val, inline=False)
            val = ""
            f = True
            for i in self.names[1]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Player", value=val, inline=False)
            self.disable_all_items()
            await interaction.edit(embed=emb, view=self)
            with open("balance.json", "r") as f:
                bal = json.load(f)
            guild = str(interaction.guild_id)
            mem = str(interaction.user.id)
            bal[guild][mem]["wallet"] = int(bal[guild][mem]["wallet"]) - self.amount
            with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)
            await interaction.message.reply(f"You lost! You have lost {self.amount} money!")
        if bust == 0:
            emb = discord.Embed(title="Blackjack")
            val = ""
            f = True
            for i in self.names[0]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Dealer", value=val, inline=False)
            val = ""
            f = True
            for i in self.names[1]:
                card = i.split("-")
                house = cards[0][int(card[0])]
                name = f"{card[1]} of {house}"
                if f is True:
                    f = False
                    val += f"{name}"
                else:
                    val += f"\n{name}"
            emb.add_field(name="Player", value=val, inline=False)
            await interaction.edit(embed=emb, view=self)


class fileselect(discord.ui.View):
    def __int__(self, user, files, total, page, inv):
        self.user = user,
        self.files = files
        self.page = page
        self.total = total
        self.inv = inv
        self.fin = False

    async def on_timeout(self):
        if self.fin is False:
            self.disable_all_items()
            embs = self.message.embeds
            await self.message.edit(embeds=embs, view=self)

    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.blurple, custom_id="file_left")
    async def _file_left(self, select, interaction): # the function called when the user is done selecting options
        emb = discord.Embed(title="Inventory")
        tfiles = None
        files = self.inv
        self.page -= 1
        if self.page <= 0:
            tfiles = self.files[f"{self.total}"]
            self.page = self.total
        else:
            tfiles = self.files[f"{self.page}"]
        if tfiles:
            for file in tfiles:
                emb.add_field(name=file, value=f"Name: {files[file]['name']}, Amount: {files[file]['amount']}",
                              inline=False)
            emb.set_footer(text=f"Page {self.page} of {self.total}")
            await interaction.response.edit_message(embed=emb, view=self)  # edit the message to show the changes)

    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.blurple, custom_id="file_right")
    async def _file_right(self, select, interaction):  # the function called when the user is done selecting options
        emb = discord.Embed(title="Inventory")
        tfiles = None
        files = self.inv
        self.page += 1
        if int(self.page) > int(self.total):
            tfiles = self.files["1"]
            self.page = 1
        else:
            tfiles = self.files[f"{self.page}"]
        if tfiles:
            for file in tfiles:
                emb.add_field(name=file, value=f"Name: {files[file]['name']}, Amount: {files[file]['amount']}",
                              inline=False)
            emb.set_footer(text=f"Page {self.page} of {self.total}")
            await interaction.response.edit_message(embed=emb, view=self)  # edit the message to show the changes)

    @discord.ui.button(emoji="❌", style=discord.ButtonStyle.blurple, custom_id="file_cancel")
    async def _file_can(self, select, interaction):  # the function called when the user is done selecting options
        self.fin = True
        self.disable_all_items()
        await interaction.response.edit_message(view=self)



async def loadinv(ctx: discord.ApplicationContext, member: discord.Member, inv):
    guild = str(ctx.guild.id)
    member = str(member.id)
    files = inv[guild][member]
    emb = discord.Embed(title="Select file")
    filebuts = fileselect()
    filebuts.page = 1
    filebuts.user = member
    total = len(files) / 10
    if total > round(total):
        total = round(total) + 1
    total = int(total)
    filebuts.total = total
    filebuts.inv = files
    numm = 0
    num = 1
    ffiles = {}
    ffiles["1"] = []
    for i, v in files.items():
        if numm >= 10:
            numm = 0
            num += 1
            page = total - num
            ffiles[f"{(total - page)}"] = []
        numm += 1
        page = total - num
        ffiles[f"{(total - page)}"].append(i)
    for file in ffiles["1"]:
        emb.add_field(name=file, value=f"Name: {files[i]['name']}, Amount: {files[i]['amount']}", inline=False)
    filebuts.files = ffiles

    await ctx.respond(embed=emb, view=filebuts)


class shopui(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=20)

    @discord.ui.select(
        placeholder = "Choose a Shop",
        min_values = 1,
        max_values = 1,
        options=[discord.SelectOption(label="axe", description="Axe Shop"),
                 discord.SelectOption(label="pickaxe", description="Pickaxe Shop")]
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        emb = discord.Embed(title=f"{select.values[0]} Shop")
        with open("shops.json", "r") as f:
                shop = json.load(f)
        store = shop[str(interaction.guild.id)]["shops"][str(select.values[0])]["items"]
        for item, value in store.items():
                emb.add_field(name=f"ID: {item} Name: {store[item]['name']} Description: {store[item]['desc']}", value=f"Price: {store[item]['price']}", inline=False)
        await interaction.response.send_message(embed=emb)

class Economy(discord.Cog):

    econ = discord.SlashCommandGroup("economy", "Economy related commands")

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @tasks.loop(seconds=5)
    async def buildtime(self):
        cont = True
        #print("loop")
        with open("builds.json", "r") as f:
             blds = json.load(f)
        with open("balance.json", "r") as f:
            bal = json.load(f)
        with open("inventory.json", "r") as f:
            inv = json.load(f)
        with open("items.json", "r") as f:
            itms = json.load(f)
        for i in blds:
            for v in blds[i]:
                for a in blds[i][v]:
                    now = datetime.datetime.utcnow().timestamp()
                    last = float(blds[i][v][a]["last"])
                    zer = timeparse("0h")
                    for b in blds[i][v][a]["production"]:
                        next = (timeparse(blds[i][v][a]["production"][b][0]) - zer) + last
                        if last == 0 or now >= next:
                            if blds[i][v][a]["reqs"] is dict:
                                for d, f in blds[i][v][a]["reqinv"].items():
                                    if int(f) >= int(blds[i][v][a]["reqs"][d]):
                                        blds[i][v][a]["reqinv"][d] = int(f) - int(blds[i][v][a]["reqs"][d])
                                    else:
                                        cont = False
                            if cont is True:
                                #print(cont)
                                blds[i][v][a]["last"] = now
                                amount = random.randint(int(blds[i][v][a]["production"][b][1][0]), int(blds[i][v][a]["production"][b][1][1]))
                                tot = 0
                                for n, m in blds[i][v][a]["export"][b].items():
                                    exlst = n.split(":")
                                    usr = exlst[0]
                                    lst = exlst[1]
                                    gvn = int(m[0])
                                    tot+=gvn
                                    if lst == "server":
                                        bal[i][v]["wallet"] = int(bal[i][v]["wallet"]) + (amount * gvn * m[1])
                                    elif lst == "inventory":
                                        if usr != v:
                                            if int(bal[i][v]["wallet"]) >= (amount * gvn * m[1]):
                                                bal[i][usr]["wallet"] = int(bal[usr][v]["wallet"]) - (amount * gvn * m[1])
                                                bal[i][v]["wallet"] = int(bal[i][v]["wallet"]) + (amount * gvn * m[1])
                                            else:
                                                inv[i][v][b]["amount"] = int(inv[i][v][b]["amount"]) + (amount * gvn)
                                        if b in inv[i][v]:
                                            inv[i][usr][b]["amount"] = int(inv[i][usr][b]["amount"]) + (amount * gvn)
                                        else:
                                            inv[i][usr][b] = itms[b]["item"]
                                            inv[i][usr][b]["amount"] = (amount * gvn)
                                    else:
                                        #print(lst)
                                        if usr in blds[i]:
                                            #print(usr)
                                            if lst in blds[i][usr]:
                                                t = blds[i][usr][lst]["reqs"]
                                                #print(type(blds[i][usr][lst]["reqs"]))
                                                if isinstance(t, dict):
                                                    #print(f"reqs: {blds[i][usr][lst]['reqs']}")
                                                    if b in blds[i][usr][lst]["reqinv"]:
                                                        if not usr == v:
                                                            if int(bal[i][v]["wallet"]) >= (amount * gvn * m[1]):
                                                                bal[i][usr]["wallet"] = int(bal[usr][v]["wallet"]) - (amount * gvn * m[1])
                                                                bal[i][v]["wallet"] = int(bal[i][v]["wallet"]) + (amount * gvn * m[1])
                                                                blds[i][usr][lst]["reqinv"][b] = int(
                                                                    blds[i][usr][lst]["reqinv"][b]) + (amount * gvn)
                                                            else:
                                                                if b in inv[i][v]:
                                                                    inv[i][v][b]["amount"] = int(inv[i][v][b]["amount"]) + (
                                                                                amount * gvn)

                                                                else:
                                                                    inv[i][v][b] = itms[b]["item"]
                                                                    inv[i][v][b]["amount"] = (amount * gvn)
                                                        else:
                                                            blds[i][v][lst]["reqinv"][b] = (
                                                                    int(blds[i][v][lst]["reqinv"][b]) + (amount * gvn))
                                                            #print("New:")
                                                            #print(blds[i][v][lst]["reqinv"][b])
                                                    else:
                                                        if b in inv[i][v]:
                                                            inv[i][v][b]["amount"] = int(inv[i][v][b]["amount"]) + (
                                                                        amount * gvn)
                                                        else:
                                                            inv[i][v][b] = itms[b]["item"]
                                                            inv[i][v][b]["amount"] = (amount * gvn)
                                                elif blds[i][usr][lst]["reqs"] is False:
                                                    if b in inv[i][v]:
                                                        inv[i][v][b]["amount"] = int(inv[i][v][b]["amount"]) + (
                                                                    amount * gvn)
                                                    else:
                                                        inv[i][v][b] = itms[b]["item"]
                                                        inv[i][v][b]["amount"] = (amount * gvn)
                                            else:
                                                if b in inv[i][v]:
                                                    inv[i][v][b]["amount"] = int(inv[i][v][b]["amount"]) + (amount * gvn)
                                                else:
                                                    inv[i][v][b] = itms[b]
                                                    inv[i][v][b]["amount"] = (amount * gvn)
                                        else:
                                            if b in inv[i][v]:
                                                inv[i][v][b]["amount"] = int(inv[i][v][b]["amount"]) + (amount * gvn)
                                            else:
                                                inv[i][v][b] = itms[b]["item"]
                                                inv[i][v][b]["amount"] = (amount * gvn)
                                if tot < 1:
                                    mkp = 1 - tot
                                    if b in inv[i][v]:
                                        inv[i][v][b]["amount"] = int(inv[i][v][b]["amount"]) + (amount * mkp)
                                    else:
                                        inv[i][v][b] = itms[b]
                                        inv[i][v][b]["amount"] = (amount * mkp)
        with open("builds.json", "w") as f:
             json.dump(blds, f, indent=4)
        with open("balance.json", "w") as f:
             json.dump(bal, f, indent=4)
        with open("inventory.json", "w") as f:
             json.dump(inv, f, indent=4)
        with open("items.json", "w") as f:
             json.dump(itms, f, indent=4)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy System Operational")
        self.buildtime.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        with open("balance.json","r") as f:
            bal = json.load(f)
        with open("inventory.json","r") as f:
            inv = json.load(f)
        with open("income.json","r") as f:
            inc = json.load(f)
        with open("shops.json", "r") as f:
            shops = json.load(f)
        
        if message.guild is None:
            return

        if not str(message.guild.id) in shops:
            shops[str(message.guild.id)] = {
                "level": 0,
                "shops": {
                    "axe": {
                        "locked": True,
                        "desc": "Axe Shop",
                        "level": 1,
                        "price": 200,
                        "owner": None,
                        "items": {
                            "axe": {
                                "name": "Axe",
                                "price": 8,
                                "level": 1,
                                "desc": "Used to chop trees"
                            },
                            "iron": {
                                "name": "Iron Axe",
                                "price": 25,
                                "level": 2,
                                "desc": "Used to chop trees"
                            },
                            "steel": {
                                "name": "Steel Axe",
                                "price": 40,
                                "level": 3,
                                "desc": "Used to chop trees"
                            }
                        }
                    },
                    "pickaxe": {
                        "locked": True,
                        "desc": "Pickaxe Shop",
                        "level": 1,
                        "price": 500,
                        "owner": None,
                        "items": {
                            "pickaxe": {
                                "name": "Pickaxe",
                                "price": 10,
                                "level": 1,
                                "desc": "Used to mine ore"
                            },
                            "iron": {
                                "name": "Iron Pickaxe",
                                "price": 30,
                                "level": 2,
                                "desc": "Used to mine ore"
                            },
                            "steel": {
                                "name": "Steel Pickaxe",
                                "price": 50,
                                "level": 3,
                                "desc": "Used to mine ore"
                            }
                        }
                    }
                }
            }

        money = 1
        if str(message.guild.id) in inc:
            for role in message.author.roles:
                if str(role.id) in inc[str(message.guild.id)]:
                    income = int(inc[str(message.guild.id)][str(role.id)]["message"])
                    money = money + income
        if not str(message.guild.id) in bal:
            bal[str(message.guild.id)] = {}
        if not str(message.channel.guild.id) in inv:
            inv[str(message.channel.guild.id)] = {}
            if not str(message.author.id) in inv[str(message.channel.guild.id)]:
                inv[str(message.channel.guild.id)][str(message.author.id)] = {}
        if not str(message.author.id) in inv[str(message.channel.guild.id)]:
            inv[str(message.channel.guild.id)][str(message.author.id)] = {}
        if str(message.author.id) in bal[str(message.guild.id)]:
            id = message.author.id
            bal[str(message.guild.id)][str(id)]["wallet"] += money
        else:
            id = message.author.id
            if not str(message.guild.id) in bal:
                bal[str(message.guild.id)] = {}
            bal[str(message.guild.id)][str(id)] = {}
            bal[str(message.guild.id)][str(id)]["wallet"] = money
            bal[str(message.guild.id)][str(id)]["bank"] = 0
        with open("shops.json","w") as f:
            json.dump(shops, f, indent=4)
        with open("balance.json", "w") as f:
            json.dump(bal, f, indent=4)
        with open("inventory.json", "w") as f:
            json.dump(inv, f, indent=4)

    @econ.command(name="shops", description="Lists what's available in the shops.")
    async def _shops(self, ctx):
        emb = discord.Embed(title="Available shops")
        await ctx.respond(embed=emb, view=shopui(bot=self.bot))

    """
    @econ.command(name="additem", description="Adds a new item to the shop")
    async def _additem(self, ctx, name: str, desc: str, price: int):
        with open("shops.json", "r") as f:
            shop = json.load(f)
        id = random.randint(000,999)
        shop[str(ctx.guild.id)]["Server"]["items"][str(id)] = {}
        shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["name"] = name
        shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["desc"] = desc
        shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["price"] = price
        shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["settings"] = {}
        shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["settings"]["addrole"] = "False"
        shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["settings"]["removerole"] = "False"
        shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["settings"]["role"] = ""
        shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["settings"]["sellable"] = "True"
        with open("shops.json", "w") as f:
            json.dump(shop, f, indent=4)
        await ctx.respond(f"Added item {shop[str(ctx.guild.id)]['Server']['items'][str(id)]['name']} with price {shop[str(ctx.guild.id)]['Server']['items'][str(id)]['price']}")
    
    @econ.command(name="edititem", description="Edits an item in the shop")
    async def _additem(self, ctx, id: int, newid: int = None, name: str = None, desc: str = None, price: int = None, addrole: bool = None, removerole: bool = None, role: discord.Role = None, sellable: bool = None):
        with open("shops.json", "r") as f:
            shop = json.load(f)
        if str(id) in shop[str(ctx.guild.id)]["Server"]["items"]:
            if newid != None:
                shop[str(ctx.guild.id)]["Server"]["items"][str(newid)] = shop[str(ctx.guild.id)]["items"][str(id)]
                shop[str(ctx.guild.id)]["Server"]["items"].pop(str(id))
            if name != None:
                shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["name"] = name
            if desc != None:
                shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["desc"] = desc
            if price != None:
                shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["price"] = price
            if addrole != None:
                shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["settings"]["addrole"] = f"{addrole}"
            if removerole != None:
                shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["settings"]["removerole"] = f"{removerole}"
            if role != None:
                shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["settings"]["role"] = f"{role.id}"
            if sellable != None:
                shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["settings"]["sellable"] = f"{sellable}"
        with open("shops.json", "w") as f:
            json.dump(shop, f, indent=4)
        await ctx.respond(f"Edited item successfully")

    @econ.command(name="removeitem", description="Removes an item from the shop")
    async def _removeitem(self, ctx, id: int):
        with open("shops.json", "r") as f:
            shop = json.load(f)
        if str(id) in shop[str(ctx.guild.id)]["Server"]["items"]:     
            name = shop[str(ctx.guild.id)]["Server"]["items"][str(id)]["name"]
            shop[str(ctx.guild.id)]["Server"]["items"].pop(str(id))
            await ctx.respond(f"Removed item {name}")
        else:
            await ctx.respond(f"Item {id} not found")
        with open("shops.json", "w") as f:
            json.dump(shop, f, indent=4)
    """
    @econ.command(name="use", description="Use an item in your inventory")
    @cooldown(1, 8, BucketType.member)
    async def use(self, ctx: discord.ApplicationContext,
                  item: discord.Option(str, description="Item to use",
                                       autocomplete=discord.utils.basic_autocomplete(get_items))):
        item = item.lower()
        with open("inventory.json", "r") as f:
            inv = json.load(f)
        with open("items.json", "r") as f:
            itms = json.load(f)
        if item in inv[str(ctx.guild.id)][str(ctx.author.id)]:
            if item in itms:
                tot = int(itms[item]["use"][0])
                chan = int(itms[item]["use"][1])
                chance = random.randint(1, tot)
                if chance > chan:
                    tps = []
                    tmplst = itms[item]["use"]
                    tmplst.pop(0)
                    tmplst.pop(0)
                    num = len(tmplst)
                    for i in range(num):
                        for x, v in tmplst[(i-1)].items():
                            if x == "reqs":
                                for b, n in v.items():
                                    if b in inv[str(ctx.guild.id)][str(ctx.author.id)]:
                                        if int(n) <= int(inv[str(ctx.guild.id)][str(ctx.author.id)][b]["amount"]):
                                            inv[str(ctx.guild.id)][str(ctx.author.id)][b]["amount"] = (
                                                    int(inv[str(ctx.guild.id)][str(ctx.author.id)][b][
                                                            "amount"]) - 1)
                                            if inv[str(ctx.guild.id)][str(ctx.author.id)][b]["amount"] <= 0:
                                                inv[str(ctx.guild.id)][str(ctx.author.id)].pop(b)
                                        else:
                                            await ctx.respond("You do not have the required materials to use this item!")
                                            return
                                    else:
                                        await ctx.respond("You do not have the required materials to use this item!")
                                        return
                            tps.append(x)
                    tp = random.choice(tps)
                    num = 0
                    for i in tmplst:
                        for x, v in i.items():
                            if x != "reqs":
                                if x == tp:
                                    num = v[1]
                    amount = random.randint(1, num)
                    if tp in inv[str(ctx.guild.id)][str(ctx.author.id)]:
                        inv[str(ctx.guild.id)][str(ctx.author.id)][tp]["amount"] = (
                            int(inv[str(ctx.guild.id)][str(ctx.author.id)][tp]["amount"]) + amount)
                    else:
                        inv[str(ctx.guild.id)][str(ctx.author.id)][tp] = itms[tp]["item"]
                    with open("inventory.json", "w") as f:
                        json.dump(inv, f, indent=4)
                    msg = itms[item]["msg"]
                    msglst1 = msg.split("{a}")
                    msg = (msglst1[0] + str(amount) + msglst1[1])
                    msglst2 = msg.split("{i}")
                    msg = (msglst2[0] + tp + msglst2[1])
                    await ctx.respond(msg)
                else:
                    await ctx.respond(f"You found nothing.")
            else:
                await ctx.respond(f"You can't use this.")

    @econ.command(name="build", description="Build a building")
    async def build(self, ctx: discord.ApplicationContext,
                    building: discord.Option(str, description="Building to build",
                                             autocomplete=discord.utils.basic_autocomplete(get_blds1))):
        with open("build.json", "r") as f:
            build = json.load(f)
        with open("builds.json", "r") as f:
             blds = json.load(f)
        with open("balance.json", "r") as f:
            bal = json.load(f)
        guild = str(ctx.guild.id)
        auth = str(ctx.author.id)
        found = False
        for i, v in build.items():
            if building.lower() == build[i]["name"].lower():
                found = True
                if int(bal[guild][auth]["wallet"]) >= int(build[i]["price"]):
                    if guild in blds:
                        if auth in blds[guild]:
                            if i in blds[guild][auth]:
                                await ctx.respond(f"You already own a {building}!")
                            else:
                                bal[guild][auth]["wallet"] = int(bal[guild][auth]["wallet"]) - int(build[i]["price"])
                                blds[guild][auth][i] = build[i]
                                disp = str(blds[guild][auth][i]["display"]).split("{u}")
                                new = ""
                                if len(disp) > 1:
                                    new = disp[0] + ctx.author.display_name + disp[1]
                                else:
                                    new = ctx.author.display_name + disp[0]
                                blds[guild][auth][i]["display"] = new
                                for z in blds[guild][auth][i]["export"]:
                                    blds[guild][auth][i]["export"][z][f"{ctx.author.id}:inventory"] = [1, 1]
                                await ctx.respond(f"You built a {building}!")
                        else:
                            blds[guild][auth] = {}
                            bal[guild][auth]["wallet"] = int(bal[guild][auth]["wallet"]) - int(build[i]["price"])
                            blds[guild][auth][i] = build[i]
                            disp = str(blds[guild][auth][i]["display"]).split("{u}")
                            new = ""
                            if len(disp) > 1:
                                new = disp[0] + ctx.author.display_name + disp[1]
                            else:
                                new = ctx.author.display_name + disp[0]
                            blds[guild][auth][i]["display"] = new
                            for z in blds[guild][auth][i]["export"]:
                                blds[guild][auth][i]["export"][z][f"{ctx.author.id}:inventory"] = [1, 1]
                            await ctx.respond(f"You built a {building}!")
                    else:
                        blds[guild] = {}
                        blds[guild][auth] = {}
                        bal[guild][auth]["wallet"] = int(bal[guild][auth]["wallet"]) - int(build[i]["price"])
                        blds[guild][auth][i] = build[i]
                        disp = str(blds[guild][auth][i]["display"]).split("{u}")
                        for z in blds[guild][auth][i]["export"]:
                            blds[guild][auth][i]["export"][z][f"{ctx.author.id}:inventory"] = [1, 1]
                        new = ""
                        if len(disp) > 1:
                            new = disp[0] + ctx.author.display_name + disp[1]
                        else:
                            new = ctx.author.display_name + disp[0]
                        blds[guild][auth][i]["display"] = new
                        await ctx.respond(f"You built a {building}!")

                    with open("builds.json", "w") as f:
                        json.dump(blds, f, indent=4)
                    with open("balance.json", "w") as f:
                        json.dump(bal, f, indent=4)

                else:
                    await ctx.respond(f"You do not have enough money to create a {building}!")
        if found is False:
            await ctx.respond("Could not find specified building.")


    """
    @econ.command(name="buy", description="Buys an item from the shop")
    async def buy(self, ctx, item: discord.Option(str, description="Item to buy",
                                                  autocomplete=discord.utils.basic_autocomplete(get_items()))):
        with open("shops.json", "r") as f:
            shop = json.load(f)
        with open("balance.json","r") as f:
            bal = json.load(f)
        if item in shop[str(ctx.guild.id)]["items"]:
            price = int(shop[str(ctx.guild.id)]["items"][str(item)]["price"])
            if int(bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"]) >= price:
                with open("inventory.json", "r") as f:
                    inv = json.load(f)
                bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"] = (
                        int(bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"]) - price)
                if str(ctx.guild.id) in inv:
                    if str(ctx.author.id) in inv[str(ctx.guild.id)]:
                        inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)] = shop[str(ctx.guild.id)]["items"][str(item)]
                    if not str(ctx.author.id) in inv[str(ctx.guild.id)]:
                        inv[str(ctx.guild.id)][str(ctx.author.id)] = {}
                        inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)] = shop[str(ctx.guild.id)]["items"][str(item)]

                else:
                    inv[str(ctx.guild.id)] = {}
                    if str(ctx.author.id) in inv[str(ctx.guild.id)]:
                        inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)] = shop[str(ctx.guild.id)]["items"][str(item)]
                    else:
                        inv[str(ctx.guild.id)][str(ctx.author.id)] = {}
                        inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)] = shop[str(ctx.guild.id)]["items"][str(item)]
                name = inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['name']
                with open("balance.json", "w") as f:
                    json.dump(bal, f, indent=4)
                with open("inventory.json", "w") as f:
                    json.dump(inv, f, indent=4)
                await ctx.respond(f"You have successfully bought item {name} for {price}")
            else:
                await ctx.respond(f"You do not have enough money for item {shop[str(ctx.guild.id)]['items'][str(item)]['name']}.")
        else:
            await ctx.respond(f"Item {item} not found")
"""

    @econ.command(name="recipes", description="All crafting recipes")
    async def recipes(self, ctx: discord.ApplicationContext):
        with open("items.json", "r") as f:
            itms = json.load(f)
        emb = discord.Embed(title="Craftable Items")
        for itm, x in itms.items():
            crft = itms[itm]["craft"]
            if isinstance(crft, dict):
                reqs = ""
                for i, v in itms[itm]["craft"]["reqs"].items():
                    reqs = reqs + f"**{i}**: {v}\n"
                emb.add_field(name=x["item"]["name"], value=reqs, inline=False)
        await ctx.respond(embed=emb)

    @econ.command(name="buildings", description="All buildings")
    async def buildings(self, ctx: discord.ApplicationContext):
        with open("build.json", "r") as f:
            bld = json.load(f)
        emb = discord.Embed(title="Buildings")
        for i, v in bld.items():
            prod = ""
            for x, c in v["production"].items():
                prod = prod + f'\nName: {x},' + ' production time: ' + c[0] + f', yield: {c[1][0]}-{c[1][1]}'
            emb.add_field(name=v["name"], value=f'**Price:** {v["price"]}, **Type:** {v["type"]}\n**Production:**{prod}', inline=False)
        await ctx.respond(embed=emb)

    @econ.command(name="built", description="All buildings you've built")
    async def built(self, ctx: discord.ApplicationContext):
        with open("builds.json", "r") as f:
            bld = json.load(f)
        emb = discord.Embed(title="Buildings")
        if not str(ctx.guild.id) in bld:
            bld[str(ctx.guild.id)] = {
                str(ctx.author.id): {}
            }
        elif not str(ctx.author.id) in bld[str(ctx.guild.id)]:
            bld[str(ctx.guild.id)][str(ctx.author.id)] = {}
            with open("builds.json", "w") as f:
                json.dump(bld, f, indent=4)
        for i, v in bld[str(ctx.guild.id)][str(ctx.author.id)].items():
            prod = ""
            exp = ""
            for x in v["export"]:
                for c, b in v["export"][x].items():
                    if int(b[0])*100 != 0:
                        exp = exp + f"\nItem: {x}, " + f"Destination: {c}, " + f"Percent: {int(b[0])*100}%, " + f"Selling at: ${b[1]}"
            for x, c in v["production"].items():
                prod = prod + f'\nName: {x},' + ' production time: ' + c[0] + f', yield: {c[1][0]}-{c[1][1]}'
            emb.add_field(name=v["display"], value=f'**Upkeep:** N/A, **Type:** {v["type"]}\n**Production:**{prod}\n**Exports:**{exp}',
                          inline=False)
        await ctx.respond(embed=emb)

    @econ.command(name="craft", description="Craft and object")
    async def craft(self, ctx: discord.ApplicationContext,
                    item: discord.Option(str, description="Item to craft", autocomplete=discord.utils.basic_autocomplete(get_crafts))):
        with open("inventory.json", "r") as f:
            inv = json.load(f)
        with open("items.json", "r") as f:
            itms = json.load(f)
        #print(item)
        if item in itms:
            if itms[item]["craft"]: # is True or itms[item]["craft"] is dict:
                #print(item)
                if str(ctx.author.id) in inv[str(ctx.guild.id)]:
                    can = True
                    for i, v in itms[item]["craft"]["reqs"].items():
                        if i in inv[str(ctx.guild.id)][str(ctx.author.id)]:
                            #print(int(inv[str(ctx.guild.id)][str(ctx.author.id)][i]["amount"]))
                            if int(v) <= int(inv[str(ctx.guild.id)][str(ctx.author.id)][i]["amount"]):
                               pass
                            else:
                                can = False
                        else:
                            can = False
                    if can is True:
                        for i, v in itms[item]["craft"]["reqs"].items():
                            inv[str(ctx.guild.id)][str(ctx.author.id)][i]["amount"] = (
                                int(inv[str(ctx.guild.id)][str(ctx.author.id)][i]["amount"]) - int(v))
                            if int(inv[str(ctx.guild.id)][str(ctx.author.id)][i]["amount"]) <= 0:
                                inv[str(ctx.guild.id)][str(ctx.author.id)].pop(i)
                        if item in inv[str(ctx.guild.id)][str(ctx.author.id)]:
                            inv[str(ctx.guild.id)][str(ctx.author.id)][item]["amount"] = (
                                    int(inv[str(ctx.guild.id)][str(ctx.author.id)][item]["amount"]) + 1)
                        else:
                            inv[str(ctx.guild.id)][str(ctx.author.id)][item] = itms[item]["item"]
                        await ctx.respond(f"You crafted a(n) {item}!")
                        with open("inventory.json", "w") as f:
                            json.dump(inv, f, indent=4)
                    else:
                        await ctx.respond("You do not have the required materials!")
                else:
                    await ctx.respond("You do not have the required materials!")
            else:
                await ctx.respond("You cannot craft this!")
        else:
            await ctx.respond("You cannot craft this!")

    @econ.command(name="export", description="Export goods from one building to another")
    async def export(self, ctx: discord.ApplicationContext,
                     item: discord.Option(str, description="Item to export",
                                          autocomplete=discord.utils.basic_autocomplete(get_exps)),
                     bld1: discord.Option(str, description="Building to export from",
                                          autocomplete=discord.utils.basic_autocomplete(get_blds)),
                     bld2: discord.Option(str, description="Building to import goods to",
                                          autocomplete=discord.utils.basic_autocomplete(get_blds)),
                     perc: discord.Option(float, description="Percent of goods to export in decimal format: e.g. 0.1 for 10%")):
        with open("builds.json", "r") as f:
            blds = json.load(f)
        with open("build.json", "r") as f:
            build = json.load(f)
        #print(perc)
        bd1 = ""
        bd2 = ""
        for x in build:
            if build[x]["name"] == bld1:
                bd1 = x
            if build[x]["name"] == bld2:
                bd2 = x
        if bld2 == "inventory" or bld2 == "server":
            bd2 = bld2
        if bld1 == "inventory" or bld1 == "server":
            await ctx.respond(f"Can't export from {bld1}")
            return
        if bd1 in blds[str(ctx.guild.id)][str(ctx.author.id)]:
            if bd2 in blds[str(ctx.guild.id)][str(ctx.author.id)] or bd2 == "inventory" or bd2 == "server":
                if bd1 != bd2:
                    if item in blds[str(ctx.guild.id)][str(ctx.author.id)][bd1]["export"]:
                        #print(item)
                        code = f"{ctx.author.id}:{bd2}"
                        blds[str(ctx.guild.id)][str(ctx.author.id)][bd1]["export"][item][code] = [perc, 0.9]
                        tot = 0
                        for i, v in blds[str(ctx.guild.id)][str(ctx.author.id)][bd1]["export"][item].items():
                            tot += float(v[0])
                        if tot == 1:
                            with open("builds.json", "w") as f:
                                json.dump(blds, f, indent=4)
                            msg = await ctx.respond(f"You are now exporting {perc*100}% of all {item}s produced by your {bld1} to your {bld2}!")
                            emb = discord.Embed(title="Export form",
                                                color=discord.Color.embed_background())
                            emb.add_field(name="Total", value=f"{tot * 100}%", inline=False)
                            for x, y in blds[str(ctx.guild.id)][str(ctx.author.id)][bd1]["export"][item].items():
                                emb.add_field(name=x, value=f"{y[0] * 100}%", inline=False)
                            await ctx.send(embed=emb)
                        else:
                            if tot < 1:
                                #print(tot)
                                #mkp = 1 - tot
                                msg = await ctx.respond(f"You are now exporting {perc * 100}% of all {item}s produced by your {bld1} to your {bld2}!")
                                #blds[str(ctx.guild.id)][str(ctx.author.id)][bd1]["export"][item][f"{ctx.author.id}:inv"][0] = float(blds[str(ctx.guild.id)][str(ctx.author.id)][bd1]["export"][item][f"{ctx.author.id}:inv"][0]) + mkp
                                emb = discord.Embed(title="Export form",
                                                    color=discord.Color.embed_background())
                                emb.add_field(name="Total", value=f"{tot * 100}%", inline=False)
                                for x, y in blds[str(ctx.guild.id)][str(ctx.author.id)][bd1]["export"][item].items():
                                    emb.add_field(name=x, value=f"{y[0] * 100}%", inline=False)
                                await ctx.send(embed=emb)
                                with open("builds.json", "w") as f:
                                    json.dump(blds, f, indent=4)
                            else:
                                emb = discord.Embed(title="Error! Exports cannot above 100%!", color=discord.Color.embed_background())
                                emb.add_field(name="Total", value=f"{tot*100}%", inline=False)
                                for x, y in blds[str(ctx.guild.id)][str(ctx.author.id)][bd1]["export"][item].items():
                                    emb.add_field(name=x, value=f"{y[0]*100}%", inline=False)
                                await ctx.respond(embed=emb)




    @econ.command(name="inventory", description="Shows your inventory")
    async def inventory(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        with open("inventory.json", "r") as f:
            inv = json.load(f)
        #emb = discord.Embed(title="Inventory", description="Shows the user's inventory")
        """
        if str(ctx.guild.id) in inv:
            if str(member.id) in inv[str(ctx.guild.id)]:
                for item, value in inv[str(ctx.guild.id)][str(member.id)].items():
                    emb.add_field(name=f"ID: {item} Name: {inv[str(ctx.guild.id)][str(member.id)][str(item)]['name']}", value=f"Price: {inv[str(ctx.guild.id)][str(member.id)][str(item)]['price']} Amount: {inv[str(ctx.guild.id)][str(member.id)][str(item)]['amount']}", inline=False)
            else:
                inv[str(ctx.guild.id)][str(member.id)] = {}
                for item, value in inv[str(ctx.guild.id)][str(member.id)].items():
                    emb.add_field(name=f"ID: {item} Name: {inv[str(ctx.guild.id)][str(member.id)][str(item)]['name']}", value=f"Price: {inv[str(ctx.guild.id)][str(member.id)][str(item)]['price']} Amount: {inv[str(ctx.guild.id)][str(member.id)][str(item)]['amount']}", inline=False)
        else:
            inv[str(ctx.guild.id)] = {}
            inv[str(ctx.guild.id)][str(member.id)] = {}
            for item, value in inv[str(ctx.guild.id)][str(member.id)].items():
                emb.add_field(name=f"ID: {item} Name: {inv[str(ctx.guild.id)][str(member.id)][str(item)]['name']}", value=f"Price: {inv[str(ctx.guild.id)][str(member.id)][str(item)]['price']} Amount: {inv[str(ctx.guild.id)][str(member.id)][str(item)]['amount']}", inline=False)
        await ctx.respond(embed=emb)
        """
        if str(ctx.guild.id) in inv:
            if str(member.id) in inv[str(ctx.guild.id)]:
                pass
            else:
                inv[str(ctx.guild.id)][str(member.id)] = {}
        else:
            inv[str(ctx.guild.id)] = {}
            inv[str(ctx.guild.id)][str(member.id)] = {}
        #await loadinv(ctx=ctx, member=member, inv=inv)
        guild = str(ctx.guild.id)
        mem = str(member.id)
        files = inv[guild][mem]
        emb = discord.Embed(title=f"{member}'s Inventory")
        filebuts = fileselect(timeout=15)
        filebuts.page = 1
        filebuts.user = mem
        total = len(files) / 10
        if total > round(total):
            total = round(total) + 1
        if len(files) > ((total*10)-10):
            total += 1
        total = int(total)
        filebuts.total = total
        filebuts.inv = files
        numm = 0
        num = 1
        ffiles = {}
        ffiles["1"] = []
        for i, v in files.items():
            if numm >= 10:
                numm = 0
                num += 1
                page = total - num
                ffiles[f"{(total - page)}"] = []
            numm += 1
            page = total - num
            ffiles[f"{(total - page)}"].append(i)
        for file in ffiles["1"]:
            emb.add_field(name=file, value=f"Name: {files[file]['name']}, Amount: {files[file]['amount']}", inline=False)
        filebuts.files = ffiles
        emb.set_footer(text=f"Page 1 of {total}")
        await ctx.respond(embed=emb, view=filebuts)


    @econ.command(name="sell", description="Sells an item")
    async def sell(self, ctx, item: discord.Option(str, description="Item to sell",
                                                   autocomplete=discord.utils.basic_autocomplete(get_items)),
                   amount: int = None):
        with open("inventory.json", "r") as f:
            inv = json.load(f)
        with open("balance.json", "r") as f:
            bal = json.load(f)
        if item:
            if amount is None:
                amount = 1
            if str(item) in inv[str(ctx.guild.id)][str(ctx.author.id)]:
                price = int(inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['price'] * amount)
                name = inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['name']
                num = int(inv[str(ctx.guild.id)][str(ctx.author.id)][str(item)]['amount'])
                if amount <= num:
                    price = price*num
                    bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"] = (
                            int(bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"]) + price)
                    inv[str(ctx.guild.id)][str(ctx.author.id)].pop(str(item))
                    await ctx.respond(f"Sold item {amount} {name}(s) for {price}!")
                else:
                    await ctx.respond(f"You do not have {amount} {name}(s)!")
        with open("inventory.json", "w") as f:
            json.dump(inv, f, indent=4)
        with open("balance.json", "w") as f:
            json.dump(bal, f, indent=4)

    @econ.command(name="fish", description="Fish for money")
    @cooldown(1, 15, BucketType.member)
    async def fish(self, ctx):
        with open("inventory.json", "r") as f:
            inv = json.load(f)
        if "cane_pole" in inv[str(ctx.guild.id)][str(ctx.author.id)]:
            final = 0
            choice = 0
            caught = False
            chance = random.randint(0, 100)
            choices = {60:{
                "name": "Boot",
                "desc": "Trash",
                "price": 10,
                "amount": 1,
                "craft": False,
                "consume": False
            }, 70:{
                "name": "Goldfish",
                "desc": "Fish",
                "price": 25,
                "amount": 1,
                "craft": False,
                "consume": False
            }, 80:{
                "name": "Bass",
                "desc": "Fish",
                "price": 35,
                "amount": 60,
                "craft": False,
                "consume": False
            }, 90:{
                "name": "Cane Pole",
                "desc": "Tool",
                "price": 8,
                "amount": 1,
                "craft": False,
                "consume": False
            }, 95:{
                "name": "Golden Fish",
                "desc": "Fish",
                "price": 120,
                "amount": 1,
                "craft": False,
                "consume": False
            }, 100:{
                "name": "Whale",
                "desc": "Tool",
                "price": 3,
                "amount": 230,
                "craft": False,
                "consume": False
            }}
            if chance == 0:
                new = (
                        int(inv[str(ctx.guild.id)][str(ctx.author.id)]["cane_pole"]["amount"]) - 1)
                if new <= 0:
                    inv[str(ctx.guild.id)][str(ctx.author.id)].pop("cane_pole")
                else:
                    inv[str(ctx.guild.id)][str(ctx.author.id)]["cane_pole"]["amount"] = new
                await ctx.respond("Your fishing pole broke!")
                with open("inventory.json", "w") as f:
                    json.dump(inv, f, indent=4)
                return
            if chance >= 60:
               # print(60)
                final = choices[60]
                caught = True
                choice = 60
            if chance >= 70:
              #  print(70)
                final = choices[70]
                caught = True
                choice = 70
            if chance >= 80:
              #  print(80)
                final = choices[80]
                caught = True
                choice = 80
            if chance >= 90:
                print(90)
                final = choices[90]
                caught = True
                choice = 90
            if chance >= 95:
              #  print(95)
                final = choices[95]
                caught = True
                choice = 95
            if chance >= 100:
              #  print(100)
                final = choices[100]
                caught = True
                choice = 100
            if caught == False:
                await ctx.respond("You didn't catch anything")
            if caught == True:
                await ctx.respond(f"You caught a {choices[choice]['name']} which is worth {choices[choice]['price']}!")
                name = final["name"].lower()
                name = name.replace(" ", "_")
                if name in inv[str(ctx.guild.id)][str(ctx.author.id)]:
                    inv[str(ctx.guild.id)][str(ctx.author.id)][name]["amount"] = int(inv[str(ctx.guild.id)][str(ctx.author.id)][name]["amount"]) + 1
                else:
                    inv[str(ctx.guild.id)][str(ctx.author.id)][name] = final
            with open("inventory.json", "w") as f:
                json.dump(inv, f, indent=4)

        else:
            await ctx.respond("You don't have a Cane Pole!")

    @econ.command(name="setmoney", description="Sets a person's wallet to an amount")
    async def setmoney(self, ctx, setting: discord.Option(str, choices=['Set', 'Add', 'Subtract']), member: discord.Member = None, amount: int = 0):
        if member is None:
            member = ctx.author
        id = member.id
        if not member.id == 614257135097872410:
            await ctx.respond("You cannot use this command")
            return
        with open("balance.json","r") as f:
            bal = json.load(f)
        if setting == "Set":
            bal[str(ctx.guild.id)][str(id)]["wallet"] = int(amount)
            await ctx.respond(f"Set {member}'s wallet to {amount}.")
        elif setting == "Add":
            bal[str(ctx.guild.id)][str(id)]["wallet"] = int(bal[str(ctx.guild.id)][str(id)]["wallet"]) + int(amount)
            await ctx.respond(f"Added {amount} to {member}'s wallet.")
        elif setting == "Subtract":
            bal[str(ctx.guild.id)][str(id)]["wallet"] = int(bal[str(ctx.guild.id)][str(id)]["wallet"]) - int(amount)
            await ctx.respond(f"Subtracted {amount} from {member}'s wallet.")

        with open("balance.json","w") as f:
            json.dump(bal, f, indent=4)

    @econ.command(name="forage", description="Forage for items")
    @cooldown(1, 15, BucketType.member)
    async def forage(self, ctx: discord.ApplicationContext,
                     item: discord.Option(str, choices=['food', 'stick', 'rock'])):
        chance = random.randint(1, 10)
        if not chance == 1:
            if not chance == 2:
                amount = random.randint(1, 3)
                with open("inventory.json", "r") as f:
                    inv = json.load(f)
                name = ""
                if item in inv[str(ctx.guild.id)][str(ctx.author.id)]:
                    inv[str(ctx.guild.id)][str(ctx.author.id)][item]["amount"] = (
                            int(inv[str(ctx.guild.id)][str(ctx.author.id)][item]["amount"]) + amount)
                    if item == "rock":
                        if amount > 1:
                            name = "rocks"
                        else:
                            name = "rock"
                    elif item == "stick":
                        if amount > 1:
                            name = "sticks"
                        else:
                            name = "stick"
                    elif item == "food":
                        if amount > 1:
                            name = "servings of food"
                        else:
                            name = "serving of food"
                else:
                    if item == "rock":
                        if amount > 1:
                            name = "rocks"
                        else:
                            name = "rock"
                        inv[str(ctx.guild.id)][str(ctx.author.id)][item] = {
                            "name": "Rock",
                            "desc": "Crafting material",
                            "price": 0.05,
                            "amount": amount,
                            "craft": True,
                            "consume": False
                        }
                    elif item == "stick":
                        if amount > 1:
                            name = "sticks"
                        else:
                            name = "stick"
                        inv[str(ctx.guild.id)][str(ctx.author.id)][item] = {
                            "name": "Stick",
                            "desc": "Crafting material",
                            "price": 0.01,
                            "amount": amount,
                            "craft": True,
                            "consume": False
                        }
                    elif item == "food":
                        if amount > 1:
                            name = "servings of food"
                        else:
                            name = "serving of food"
                        inv[str(ctx.guild.id)][str(ctx.author.id)][item] = {
                            "name": "Food",
                            "desc": "Consumable",
                            "price": 0.5,
                            "amount": amount,
                            "craft": False,
                            "consume": True
                        }
                with open("inventory.json", "w") as f:
                    json.dump(inv, f, indent=4)
                await ctx.respond(f"You found {amount} {name}!")
            else:
                await ctx.respond("You found nothing")

        else:
            await ctx.respond("You found nothing")

    """
    @econ.command(name="daily", description="Gives you, your daily wage")
    @commands.cooldown(rate=1, per=86400, type=commands.BucketType.member)
    async def daily(self, ctx: discord.ApplicationContext):
        with open("income.json","r") as f:
            inc = json.load(f)
        with open("balance.json","r") as f:
            bal = json.load(f)
        money = random.randint(30, 100)
        if str(ctx.guild.id) in inc:
            for role in ctx.author.roles:
                if str(role.id) in inc[str(ctx.guild.id)]:
                    income = int(inc[str(ctx.guild.id)][str(role.id)]["daily"])
                    money = money + income

        if str(ctx.author.id) in bal[str(ctx.guild.id)]:
            bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"] = int(bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"]) + money
        else:
            bal[str(ctx.guild.id)][str(ctx.author.id)] = {}
            bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"] = 0
            bal[str(ctx.guild.id)][str(ctx.author.id)]["bank"] = 0
            bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"] = int(bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"]) + money
        with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)
        await ctx.respond(f"You have been awarded {money} for your daily use.")
    
    @econ.command(name="incomerole", description="Adds a role to increase income")
    async def addincomerole(self, ctx, role: discord.Role, setting: discord.Option(str, choices=['Add', 'Remove']), daily: bool = None, dailyamount: int = None, message: bool = None, messageamount: int = None):
        with open("income.json","r") as f:
            inc = json.load(f)
        if str(ctx.guild.id) not in inc:
            inc[str(ctx.guild.id)] = {}
        print(daily)
        print(dailyamount)
        print(message)
        print(messageamount)
        if setting == "Add":
            if daily == True and dailyamount is not None:
                if message == False or message is None:
                    if str(role.id) not in inc[str(ctx.guild.id)]:
                        inc[str(ctx.guild.id)][str(role.id)] = {}
                        inc[str(ctx.guild.id)][str(role.id)]["daily"] = int(dailyamount)
                        inc[str(ctx.guild.id)][str(role.id)]["message"] = 0

                        await ctx.respond(f"Added {role.name} to income list with daily amount {dailyamount}.")
                    else:
                        inc[str(ctx.guild.id)][str(role.id)]["daily"] = int(dailyamount)
                        await ctx.respond(f"Eddited {role.name} in income list. Changed daily amount to {dailyamount}.")
                    with open("income.json","w") as f:
                        json.dump(inc, f, indent=4)
            elif message == True and messageamount is not None:
                if daily == False or daily is None:
                    if str(role.id) not in inc[str(ctx.guild.id)]:
                        inc[str(ctx.guild.id)][str(role.id)] = {}
                        inc[str(ctx.guild.id)][str(role.id)]["daily"] = 0
                        inc[str(ctx.guild.id)][str(role.id)]["message"] = int(messageamount)

                        await ctx.respond(f"Added {role.name} to income list with message amount {messageamount}.")
                    else:
                        inc[str(ctx.guild.id)][str(role.id)]["message"] = int(messageamount)
                        await ctx.respond(f"Eddited {role.name} in income list. Changed message amount to {messageamount}.")
                    with open("income.json","w") as f:
                        json.dump(inc, f, indent=4)
            elif daily == True and message == True and dailyamount is not None and messageamount is not None:
                if str(role.id) not in inc[str(ctx.guild.id)]:
                    inc[str(ctx.guild.id)][str(role.id)] = {}
                    inc[str(ctx.guild.id)][str(role.id)]["daily"] = int(dailyamount)
                    inc[str(ctx.guild.id)][str(role.id)]["message"] = int(messageamount)
                    await ctx.respond(f"Added {role.name} to income list with message amount {messageamount} and daily amount {dailyamount}.")
                else:
                    inc[str(ctx.guild.id)][str(role.id)]["message"] = int(messageamount)
                    inc[str(ctx.guild.id)][str(role.id)]["daily"] = int(dailyamount)
                    await ctx.respond(f"Eddited {role.name} in income list. Changed message amount to {messageamount} and daily amoun to {dailyamount}.")
                with open("income.json","w") as f:
                    json.dump(inc, f, indent=4)
            else:
                await ctx.respond(f"You need to specify a daily amount or a message amount.")
        if setting == "Remove":
            if str(role.id) not in inc[str(ctx.guild.id)]:
                await ctx.respond(f"{role.name} is not in the income list.")
            else:
                inc[str(ctx.guild.id)].pop(str(role.id))
                await ctx.respond(f"{role.name} has been removed from list.")
            with open("income.json","w") as f:
                json.dump(inc, f, indent=4)
"""
    @econ.command(name="balance",description="Shows a person's balance")
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        id = member.id
        with open("balance.json","r") as f:
            bal = json.load(f)
        if str(id) in bal[str(ctx.guild.id)]:
            emb = discord.Embed(title=f"{member}'s Balance")
            emb.add_field(name="Wallet", value=bal[str(ctx.guild.id)][str(id)]["wallet"])
            emb.add_field(name="Bank", value=bal[str(ctx.guild.id)][str(id)]["bank"])
            await ctx.respond(embed=emb)
        else:
            bal[str(ctx.guild.id)][str(id)] = {}
            bal[str(ctx.guild.id)][str(id)]["wallet"] = 0
            bal[str(ctx.guild.id)][str(id)]["bank"] = 0
            with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)
            emb = discord.Embed(title=f"{member}'s Balance")
            emb.add_field(name="Wallet", value=bal[str(ctx.guild.id)][str(id)]["wallet"])
            emb.add_field(name="Bank", value=bal[str(ctx.guild.id)][str(id)]["bank"])
            await ctx.respond(embed=emb)

    @econ.command(name="deposit",description="Deposis money into your bank")
    async def deposit(self, ctx, amount: int):
        member = ctx.author
        id = member.id
        with open("balance.json","r") as f:
            bal = json.load(f)
        if str(id) in bal[str(ctx.guild.id)]:
            if bal[str(ctx.guild.id)][str(id)]["wallet"] >= amount:
                bal[str(ctx.guild.id)][str(id)]["wallet"] = int(bal[str(ctx.guild.id)][str(id)]["wallet"]) - int(amount)
                bal[str(ctx.guild.id)][str(id)]["bank"] = int(bal[str(ctx.guild.id)][str(id)]["bank"]) + int(amount)

                await ctx.respond(f"You have successfully deposited {amount} into your bank.")
            else:
                await ctx.respond("You do not have enough money in your wallet.")
        else:
            bal[str(ctx.guild.id)][str(id)] = {}
            bal[str(ctx.guild.id)][str(id)]["wallet"] = 1
            bal[str(ctx.guild.id)][str(id)]["bank"] = 0
            if bal[str(ctx.guild.id)][str(id)]["wallet"] >= amount:
                bal[str(ctx.guild.id)][str(id)]["wallet"] = int(bal[str(ctx.guild.id)][str(id)]["wallet"]) - int(amount)
                bal[str(ctx.guild.id)][str(id)]["bank"] = int(bal[str(ctx.guild.id)][str(id)]["bank"]) + int(amount)
                await ctx.respond(f"You have successfully deposited {amount} into your bank.")
        with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)

    @econ.command(name="withdraw",description="Withdraws money from your bank")
    async def withdraw(self, ctx, amount: int):
        member = ctx.author
        id = member.id
        with open("balance.json","r") as f:
            bal = json.load(f)
        if str(id) in bal[str(ctx.guild.id)]:
            if bal[str(ctx.guild.id)][str(id)]["bank"] >= amount:
                bal[str(ctx.guild.id)][str(id)]["bank"] = int(bal[str(ctx.guild.id)][str(id)]["bank"]) - int(amount)
                bal[str(ctx.guild.id)][str(id)]["wallet"] = int(bal[str(ctx.guild.id)][str(id)]["wallet"]) + int(amount)
                await ctx.respond(f"You have successfully withdrawn {amount} from your bank.")
            else:
                await ctx.respond("You do not have enough money in your bank.")
        else:
            bal[str(ctx.guild.id)][str(id)] = {}
            bal[str(ctx.guild.id)][str(id)]["wallet"] = 1
            bal[str(ctx.guild.id)][str(id)]["bank"] = 0
            if bal[str(ctx.guild.id)][str(id)]["bank"] >= amount:
                bal[str(ctx.guild.id)][str(id)]["bank"] = int(bal[str(ctx.guild.id)][str(id)]["bank"]) - int(amount)
                bal[str(ctx.guild.id)][str(id)]["wallet"] = int(bal[str(ctx.guild.id)][str(id)]["wallet"]) + int(amount)
                await ctx.respond(f"You have successfully withdrawn {amount} from your bank.")
        with open("balance.json", "w") as f:
                json.dump(bal, f, indent=4)

    @econ.command(name="blackjack", description="Gamble your money through Blackjack")
    async def blackjack(self, ctx: discord.ApplicationContext, amount: int):
        with open("balance.json","r") as f:
            bal = json.load(f)
        with open("inventory.json", "r") as f:
            inv = json.load(f)
        if "blackjack" in inv[str(ctx.guild.id)][str(ctx.author.id)]:
            if int(bal[str(ctx.guild.id)][str(ctx.author.id)]["wallet"]) >= amount:
                used = []
                deal = [0, 0]
                user = [0, 0]
                for i in range(4):
                    find = False
                    card = None
                    while find is False:
                        house = random.randint(0, 3)
                        card = random.choice(list(cards[1].keys()))
                        name = f"{house}-{card}"
                        if not name in used:
                            used.append(name)
                            find = True
                    if i < 2:
                        num = cards[1][card]
                        deal[0] += num[0]
                        deal[1] += num[1]
                    else:
                        num = cards[1][card]
                        user[0] += num[0]
                        user[1] += num[1]
                emb = discord.Embed(title="Blackjack")
                for i in range(2):
                    if i == 0:
                        card = used[0].split("-")
                        card1 = used[1].split("-")
                        house = cards[0][int(card[0])]
                        house1 = cards[0][int(card1[0])]
                        name = f"{card[1]} of {house}"
                        name1 = f"{card1[1]} of {house1}"
                        emb.add_field(name="Dealer", value=f"{name}\n{name1}", inline=False)
                    else:
                        card = used[2].split("-")
                        card1 = used[3].split("-")
                        house = cards[0][int(card[0])]
                        house1 = cards[0][int(card1[0])]
                        name = f"{card[1]} of {house}"
                        name1 = f"{card1[1]} of {house1}"
                        emb.add_field(name="Player", value=f"{name}\n{name1}", inline=False)
                view = blackview(used=used, deal=deal, user=user, amount=amount)
                await ctx.respond(embed=emb, view=view)
            else:
                await ctx.respond("You do not have enough money to gamble")
        else:
            await ctx.respond("You must have the blackjack item.")


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Economy(bot)) # add the cog to the bot
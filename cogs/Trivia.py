import discord
import json
import random
import configparser

config = configparser.ConfigParser()
confile = config.read("config.conf")
conf = config.get('config', 'trivia')
allowed = conf.split(',')

class sel(discord.ui.Select):
    def __init__(self, files, total, page, opts):
        #self.bot = bot
        self.files = files
        self.page = page
        self.total = total
        super().__init__(options=opts)

    async def callback(self, interaction: discord.Interaction):
        with open("trivia.json", "r") as f:
            triv = json.load(f)
        num = self.values[0]
        orgembs = interaction.message.embeds
        emb = discord.Embed(title=f"Remove question {num}?",
                            description=f"Question: {triv[num]['ques']}, Answers: {triv[num]['ans']}, "
                                               f"Correct: {get_ans(triv, num)}",color=discord.Color.embed_background())
        comf = numcomf()
        comf.files = self.files
        comf.file = num
        comf.page = self.page
        comf.total = self.total
        comf.embeds = orgembs
        comf.opts = self.options
        await interaction.response.edit_message(embed=emb, view=comf)

class numselect(discord.ui.View):
    def __int__(self, files, total, page):
        self.files = files
        self.page = page
        self.total = total
        super().__init__(timeout=20)

    @discord.ui.button(emoji="??", style=discord.ButtonStyle.blurple, custom_id="trivia_back")
    async def _file_back(self, button, interaction): # the function called when the user is done selecting options
        select = fileselect()
        select.files = self.files
        select.page = int(self.page)
        select.total = int(self.total)
        await interaction.response.edit_message(view=select)

    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(view=self)


class numcomf(discord.ui.View):
    def __int__(self, files, total, page, embeds, file, opts):
        self.files = files
        self.page = page
        self.total = total
        self.embeds = embeds
        self.file = file
        self.opts = opts
        super().__init__(timeout=None)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="trivia_yes")
    async def _triviayes(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.disable_all_items()
        with open("trivia.json", "r") as f:
            triv = json.load(f)
        triv.pop(self.file)
        with open("trivia.json", "w") as f:
            json.dump(triv, f, indent=4)
        emb = discord.Embed(title=f"You have deleted question {self.file}",color=discord.Color.embed_background())
        #emb = discord.Embed(title=f"Unassigned {self.choice}s/{self.file} to {self.user.name}")
        await interaction.response.edit_message(embed=emb, view=self)


    @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="trivia_no")
    async def _triviano(self, button: discord.ui.Button, interaction: discord.Interaction):
        select = numselect()
        select.files = self.files
        select.file = self.file
        select.page = self.page
        select.total = self.total
        select.add_item(sel(files=self.files,page=self.page,total=self.total,opts=self.opts))
        await interaction.response.edit_message(embeds=self.embeds, view=select)

class fileselect(discord.ui.View):
    def __int__(self, files, total, page):
        self.files = files
        self.page = page
        self.total = total

    @discord.ui.button(emoji="??", style=discord.ButtonStyle.blurple, custom_id="trivia_left")
    async def _trivia_left(self, select, interaction): # the function called when the user is done selecting options
        emb = discord.Embed(title="Trivia questions",color=discord.Color.embed_background())
        with open("trivia.json", "r") as f:
            triv = json.load(f)
        tfiles = None
        with open("trivia.json", "r") as f:
            triv = json.load(f)
        self.page -= 1
        if self.page <= 0:
            tfiles = self.files[f"{self.total}"]
            self.page = self.total
        else:
            tfiles = self.files[f"{self.page}"]
        if tfiles:
            for file in tfiles:
                emb.add_field(name=file, value=f"Question: {triv[file]['ques']}, Answers: {triv[file]['ans']}, "
                                               f"Correct: {get_ans(triv, file)}",
                              inline=False)
            emb.set_footer(text=f"Page {self.page} of {self.total}")
            await interaction.response.edit_message(embed=emb, view=self)  # edit the message to show the changes)

    @discord.ui.button(emoji="??", style=discord.ButtonStyle.blurple, custom_id="trivia_right")
    async def _trivia_right(self, select, interaction):  # the function called when the user is done selecting options
        emb = discord.Embed(title="Trivia questions",color=discord.Color.embed_background())
        with open("trivia.json", "r") as f:
            triv = json.load(f)
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
                emb.add_field(name=file, value=f"Question: {triv[file]['ques']}, Answers: {triv[file]['ans']}, "
                                               f"Correct: {get_ans(triv, file)}",
                              inline=False)
            emb.set_footer(text=f"Page {self.page} of {self.total}")
            await interaction.response.edit_message(embed=emb, view=self)  # edit the message to show the changes)

    @discord.ui.button(emoji="??", style=discord.ButtonStyle.blurple, custom_id="trivia_ok")
    async def _trivia_ok(self, select, interaction):  # the function called when the user is done selecting options
        buts = numselect()
        buts.files = self.files
        buts.page = self.page
        buts.total = self.total
        opts = []
        for i in self.files[str(buts.page)]:
            opts.append(discord.SelectOption(
                label=i
            ))
        buts.add_item(sel(files=self.files, page=self.page, total=self.total, opts=opts))
        await interaction.response.edit_message(view=buts)

    @discord.ui.button(emoji="?", style=discord.ButtonStyle.blurple, custom_id="trivia_cancel")
    async def _file_can(self, select, interaction):  # the function called when the user is done selecting options
        self.disable_all_items()
        await interaction.response.edit_message(view=self)

def get_ans(triv, file):
    cors = []
    for i, v in triv[file]["ans"].items():
        if v == 1:
            cors.append(i)
    return cors

def get_id(triv):
    found = False
    while not found:
        num = random.randint(000,999)
        if not str(num) in triv:
            found = triv
            return num


class View(discord.ui.View):
    def __init__(self, ques):
        self.ques = ques
        super().__init__(timeout=10)

    async def on_timeout(self):
        self.disable_all_items()
        self.msg = self.message
        embs = self.msg.embeds
        emb = embs[0]
        emb = emb.set_footer(text="You didn't answer fast enough!")
        #embs.append(emb)
        with open("trivia.json", "r") as f:
            triv = json.load(f)
        triv[str(self.ques)]["use"] = 0
        with open("trivia.json", "w") as f:
            json.dump(triv, f, indent=4)
        await self.message.edit(embed=emb, view=self)
        self.stop()


class Button(discord.ui.Button):
    def __init__(self, label, ques, cust):
        #self.bot = bot
        self.ques = ques
        super().__init__(label=label, style=discord.ButtonStyle.grey, custom_id=cust)

    async def callback(self, interaction: discord.Interaction):
        with open("trivia.json", "r") as f:
            triv = json.load(f)
        correct = triv[str(self.ques)]["ans"][str(self.label)]
        if correct == 1:
            self.style = discord.ButtonStyle.green
            embs = interaction.message.embeds
            emb = embs[0]
            emb.set_footer(text=f"{interaction.user.name} is correct!")
        else:
            self.style = discord.ButtonStyle.red
            for i, v in triv[str(self.ques)]["ans"].items():
                if v == 1:
                    but = self.view.get_item(i)
                    but.style = discord.ButtonStyle.green
            embs = interaction.message.embeds
            emb = embs[0]
            emb.set_footer(text=f"{interaction.user.name} is wrong!")
        self.view.disable_all_items()
        await interaction.response.edit_message(embed=emb, view=self.view)
        self.view.stop()


class Trivia(discord.Cog):

    def __init__(self, bot):
        self.bot = bot

    triv = discord.SlashCommandGroup("trivia", "Trivia related commands")

    @triv.command(name="play", description="Play trivia")
    async def trivia(self, ctx: discord.ApplicationContext):
        await ctx.respond("Getting question..", ephemeral=True)
        with open("trivia.json", "r") as f:
            triv = json.load(f)
        lst = []
        for i, v in triv.items():
            if triv[i]["use"] == 0:
                lst.append(i)
        if lst == []:
            for i, v in triv.items():
                triv[i]["use"] = 0
                lst.append(i)
        ques = random.choice(lst)
        triv[ques]["use"] = 1
        with open("trivia.json", "w") as f:
            json.dump(triv, f, indent=4)
        lsst = []
        for i, v in triv[ques]["ans"].items():
            lsst.append(i)
        view = View(ques=ques)
        random.shuffle(lsst)
        for i in lsst:
            view.add_item(Button(label=i, ques=ques, cust=i))
        emb = discord.Embed(title=triv[ques]["ques"], description="Answer this question within 10 seconds!",
                            color=discord.Color.embed_background())
        await ctx.send(embed=emb, view=view)

    @triv.command(name="remove", description="removes a trivia question")
    async def remtrivia(self, ctx: discord.ApplicationContext):
        if str(ctx.author.id) in allowed:
            with open("trivia.json", "r") as f:
                triv = json.load(f)
            emb = discord.Embed(title="Trivia questions")
            filebuts = fileselect()
            filebuts.page = 1
            total = len(triv) / 10
            if total > round(total):
                total = int(round(total) + 1)
            else:
                total = round(total)
            filebuts.total = total
            filebuts.inv = triv
            numm = 0
            num = 1
            ffiles = {}
            ffiles["1"] = []
            for i, v in triv.items():
                if numm >= 10:
                    numm = 0
                    num += 1
                    page = total - num
                    ffiles[f"{(total - page)}"] = []
                numm += 1
                page = total - num
                ffiles[f"{(total - page)}"].append(i)
            for file in ffiles["1"]:
                emb.add_field(name=file, value=f"Question: {triv[file]['ques']}, Answers: {triv[file]['ans']}, "
                                               f"Correct: {get_ans(triv,file)}",
                              inline=False)
            filebuts.files = ffiles
            emb.set_footer(text=f"Page 1 of {total}")
            await ctx.respond(embed=emb, view=filebuts)
        else:
            emb = discord.Embed(title="You can not use this command!", color=discord.Color.from_rgb(43,45,49))
            await ctx.respond(embed=emb)

    @triv.command(name="add", description="adds a trivia question")
    async def addtrivia(self, ctx, question, answers: str, correct: str):
        if str(ctx.author.id) in allowed:
            with open("trivia.json", "r") as f:
                triv = json.load(f)
            lst = answers.split(",")
            correct = correct.split(",")
            num = get_id(triv)
            new = {
                "use": 0,
                "ques": question,
                "ans": {}
            }
            cors = []
            for i in lst:
                for v in correct:
                    if i == lst[(int(v)-1)]:
                        cors.append(lst[(int(v)-1)])
                        new["ans"][i] = 1
                    else:
                        if str(i) in cors:
                            pass
                        else:
                            new["ans"][i] = 0
            triv[str(num)] = new
            with open("trivia.json", "w") as f:
                json.dump(triv, f, indent=4)
            emb = discord.Embed(title="Added trivia!", color=discord.Color.embed_background())
            emb.add_field(name="Question", value=question, inline=False)
            emb.add_field(name="Answers", value=str(lst), inline=False)
            emb.add_field(name="Correct Answers", value=str(cors), inline=False)
            await ctx.respond(embed=emb)


def setup(bot):
    bot.add_cog(Trivia(bot))
import discord
from discord.ext import commands

letters = {'a': "A", 'b': "B", 'c': "C", 'd': "D", 'e': "E", 'f': "F", 'g': "G", 'h': "H", 'i': "I", 'j': "J", 'k': "K", 'l': "L", 'm': "M", 'n': "N", 'o': "O", 'p': "P", 'q': "Q", 'r': "R", 's': "S", 't': "T", 'u': "U", 'v': "V", 'w': "W", 'x': "X", 'y': "Y", 'z': "Z"}


class View(discord.ui.View):
    def __init__(self, emb):
        super().__init__(timeout=30)
        self.emb = emb

    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(embed=self.emb, view=self)


class Select(discord.ui.Select):
    def __init__(self, opts, dic):
        self.dic = dic
        super().__init__(placeholder="Select an option", min_values=1, max_values=1, options=opts, select_type=discord.ComponentType.string_select)

    async def callback(self, interaction: discord.Interaction):
        name = self.values[0]
        if name.lower() == "help":
            sname = name
            desc = "Main help screen"
        else:
            desc = self.dic[name.lower()]["DESC"]
            lets = [*name.lower()]
            frst = letters[lets[0]]
            lets.pop(0)
            new = frst
            for i in lets:
                new+=i
            sname = f"Help {new}"
        emb = discord.Embed(title=sname, description=desc, color=discord.Color.embed_background())
        if name.lower() == "help":
            for i in self.dic:
                if not i == "misc":
                    emb.add_field(name=f"/{i}", value=self.dic[i]["DESC"], inline=False)
            emb.add_field(name=f"Misc", value="Miscellaneous commands", inline=False)
            self.view.emb = emb
            await interaction.response.edit_message(embed=emb, view=self.view)
        else:
            for i, v in self.dic[name.lower()].items():
                if not i == "DESC":
                    emb.add_field(name=f"/{i}", value=v, inline=False)
            self.view.emb = emb
            await interaction.response.edit_message(embed=emb, view=self.view)

class Help(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot: discord.Bot = bot

    #cmds = discord.SlashCommandGroup(name="help", description="help fuction", guild_ids=[898697869580730429])

    @discord.slash_command(name="help", description="Returns all commands") # we can also add application commands
    async def help(self, ctx: discord.ApplicationContext):
        emb = discord.Embed(title="Help", color=discord.Color.embed_background())
        dic = {}
        for cmd in self.bot.walk_application_commands():
            if not cmd.qualified_name in dic:
                par = str(cmd.parent)
                parl = par.split(" ")
                par = parl[0]
                des = "None"
                if cmd.parent:
                    des = str(cmd.parent.description)
                if par.lower() == "none":
                    par = "misc"
                if par in dic:
                    dic[par][cmd.qualified_name] = cmd.description
                else:
                    if par == "misc":
                        des = "Miscellaneous commands"
                    dic[par] = {
                        "DESC": des,
                        cmd.qualified_name: cmd.description
                    }
        opts = []
        opts.append(discord.SelectOption(label="Help", description="Main help screen"))
        for i in dic:
            if not i == "misc":
                opts.append(discord.SelectOption(label=i, description=dic[i]["DESC"]))
                emb.add_field(name=f"/{i}", value=dic[i]["DESC"], inline=False)
        opts.append(discord.SelectOption(label="Misc", description="Miscellaneous commands"))
        emb.add_field(name=f"Misc", value="Miscellaneous commands", inline=False)
        view = View(emb=emb)
        view.add_item(Select(opts=opts, dic=dic))
        await ctx.respond(embed=emb, view=view)


def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Help(bot)) # add the cog to the bot


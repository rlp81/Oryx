import discord
from discord.ext import commands

class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

class Link(discord.ui.Button):
    def __init__(self, url):
        super().__init__(label="Download Avatar", style=discord.ButtonStyle.link, url=url)

class Fun(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    av = discord.SlashCommandGroup(name="avatar", description="Profile avatars")

    @av.command(name="user",description="Returns a user's avatar") # we can also add application commands
    async def sus(self, ctx: discord.ApplicationContext, member: discord.Member = None):
        if not member:
            member = ctx.author
        emb = discord.Embed(title=f"{member}'s Avatar", url=member.avatar.url)
        emb.set_image(url=member.avatar.url)
        view = View()
        view.add_item(Link(url=member.avatar.url))
        await ctx.respond(embed=emb, view=view)

    @av.command(name="server", description="Returns the server's icon")  # we can also add application commands
    async def sus(self, ctx: discord.ApplicationContext):
        guild = ctx.guild
        if guild.icon:
            emb = discord.Embed(title=f"{guild.name} icon", url=guild.icon.url)
            emb.set_image(url=guild.icon.url)
            view = View()
            view.add_item(Link(url=guild.icon.url))
            await ctx.respond(embed=emb, view=view)
        else:
            await ctx.respond("Server has no icon", ephemeral=True)




def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Fun(bot)) # add the cog to the bot


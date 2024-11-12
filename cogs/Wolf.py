import discord
from discord.ext import commands
import wolframalpha
import configparser

config = configparser.ConfigParser()
confile = config.read("config.conf")
app = config.get('config', 'wolfram')

wolfclient = wolframalpha.Client(app)

class Wolf(discord.Cog):
    def __init__(self, bot):
        self.bot = bot

    #fun = discord.SlashCommandGroup("fun", "Fun commands!")

    @discord.command(name="ask", description="Responds to a scholarly question")
    async def ask(self, ctx: discord.ApplicationContext, prompt):
        await ctx.defer()
        try:
            res = await wolfclient.aquery(prompt)
            answer = next(res.results).text
            emb = discord.Embed(title=prompt, description=answer, color=discord.Color.embed_background())
            emb.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.respond(embed=emb)
        except Exception as e:
            print(e)
            emb = discord.Embed(title=prompt, description=f"Apologies I encountered an error\n{e}", color=discord.Color.embed_background())
            emb.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.respond(embed=emb)


def setup(bot):
    bot.add_cog(Wolf(bot))

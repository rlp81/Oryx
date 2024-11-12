import discord
from discord import option
from discord.ext import commands
from discord.ext.commands import has_permissions
import json


class settings(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message or not message.guild:
            return
        with open("guilds.json", "r") as f:
            guilds = json.load(f)
        if not str(message.guild.id) in guilds:
            guilds[str(message.guild.id)] = {
                "over18": False
            }
        with open("guilds.json", "w") as f:
            json.dump(guilds, f, indent=4)

    @discord.slash_command(name="settings",description="Change server settings") # we can also add application commands
    @has_permissions(administrator=True)
    @option("over18", description="Allows 18+ reddit memes")
    async def settings(self, ctx, over18: bool = None):
        if over18 != None:
            with open("guilds.json", "r") as f:
                guilds = json.load(f)
            if str(ctx.guild.id) in guilds:
                guilds[str(ctx.guild.id)]["over18"] = f"{over18}"
            else:
                guilds[str(ctx.guild.id)] = {}
                guilds[str(ctx.guild.id)]["over18"] = f"{over18}"
            with open("guilds.json", "w") as f:
                json.dump(guilds, f, indent=4)
            
            await ctx.respond(f"Changed setting over18 to {over18}")
        else:
            await ctx.respond("Please specify what you want to change")

    @discord.slash_command(name="channel", description="Sets channels")
    @has_permissions(manage_channels=True)
    async def channel(self, ctx, channeltype: discord.Option(str, choices=['welcome', 'leave', 'log', 'youtube', 'pin']), textchannel: discord.TextChannel = None):

        guild = ctx.guild
        if textchannel is None:
            textchannel = ctx.channel
        with open("channels.json", "r") as f:
            chans = json.load(f)
        if not str(guild.id) in chans:
            chans[str(guild.id)] = {}
            chans[str(guild.id)]["welcome"] = 0
            chans[str(guild.id)]["leave"] = 0
            chans[str(guild.id)]["log"] = 0
            chans[str(guild.id)]["yt"] = 0
            chans[str(guild.id)]["cad"] = 0
            chans[str(guild.id)]["pin"] = 0
            chans[str(guild.id)]["black"] = []
            chans[str(guild.id)]["roles"] = []
        chans[str(guild.id)][channeltype] = textchannel.id
        await ctx.respond(f"Changed {channeltype} channel to {textchannel.mention}")
        with open("channels.json", "w") as f:
            json.dump(chans, f, indent=4)

    @discord.slash_command(name="blacklist", description="Blacklists the bot from logging messages from a channel")
    @has_permissions(manage_channels=True)
    async def blacklist(self, ctx: discord.ApplicationContext, setting: discord.Option(str, choices=["add", "remove", "list"]), channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        guild = ctx.guild
        with open("channels.json", "r") as f:
            chans = json.load(f)
        if not str(guild.id) in chans:
            chans[str(guild.id)] = {}
            chans[str(guild.id)]["welcome"] = 0
            chans[str(guild.id)]["leave"] = 0
            chans[str(guild.id)]["log"] = 0
            chans[str(guild.id)]["yt"] = 0
            chans[str(guild.id)]["black"] = []
            chans[str(guild.id)]["roles"] = []
        if setting.lower() == "add":
            if not str(channel.id) in chans[str(guild.id)]["black"]:
                chans[str(guild.id)]["black"].append(str(channel.id))
                await ctx.respond(f"Added {channel.name} to logging blacklist")
            else:
                await ctx.respond(f"Channel {channel.name} already on logging blacklist")
        elif setting.lower() == "remove":
            if str(channel.id) in chans[str(guild.id)]["black"]:
                chans[str(guild.id)]["black"].remove(str(channel.id))
                await ctx.respond(f"Channel {channel.name} has been removed from logging blacklist")
            else:
                await ctx.respond(f"{channel.name} is not on logging blacklist")
        elif setting.lower() == "list":
            txt = ""
            for i in chans[str(guild.id)]["black"]:
                if txt == "":
                    txt = guild.get_channel(int(i)).name
                else:
                    txt += f"\n{guild.get_channel(int(i)).name}"
            emb = discord.Embed(title="Logging blacklist", description=txt)
            await ctx.respond(embed=emb)
        with open("channels.json", "w") as f:
            json.dump(chans, f, indent=4)
            

def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(settings(bot))  # add the cog to the bot

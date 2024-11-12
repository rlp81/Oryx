import discord
from discord.ext import commands
import os
import json
from easy_pil import Editor, Canvas, load_image_async, Font

class Guilds(discord.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot: discord.Bot = bot

    serv = discord.SlashCommandGroup(name="serverinfo", guild_ids=[866127811000401921])

    @serv.command(name="joinboard", guild_ids=[898697869580730429])
    async def joinboard(self, ctx: discord.ApplicationContext):
        member = ctx.author
        guild = ctx.guild
        background = Editor(Canvas((900, 500), color="#242424"))
        front = Editor(Canvas((800, 400), color="#141414")).rounded_corners()
        front.rectangle((312.5, 37.5), 175, 175, color="#fff0ab", radius=175)
        front.rectangle((315, 40), 170, 170, color="#141414", radius=170)
        background.paste(front, (50, 50))
        prof_pict = await load_image_async(str(member.avatar.url))
        profile = Editor(prof_pict).resize((150, 150)).circle_image()
        poppins = Font.poppins(size=50)
        poppins_sml = Font.poppins(size=30)
        background.paste(profile, (375, 100))
        background.text((450, 300), f"{member} has joined!", font=poppins, color="#FFFFFF", align="center")
        background.text((450, 375), f"Welcome to {guild.name}!", font=poppins_sml, color="#FFFFFF", align="center")
        await ctx.respond(file=discord.File(fp=background.image_bytes, filename="join_card.png"))

    @serv.command(name="guilds", guild_ids=[866127811000401921])
    async def guilds(self, ctx: discord.ApplicationContext):
        text = ""
        for guild in self.bot.guilds:
            if text == "":
                text += f"{guild.id}-{guild.name}"
            else:
                text += f"\n{guild.id}-{guild.name}"
        with open("glds.txt", "w") as f:
            f.write(text)
        await ctx.respond("Sent", ephemeral=True)
        await ctx.author.send(file=discord.File(f"{os.getcwd()}/glds.txt"))
        os.remove(f"{os.getcwd()}/glds.txt")

    @serv.command(name="channels", guild_ids=[866127811000401921])
    async def channels(self, ctx: discord.ApplicationContext, guildid: str):
        guild = self.bot.get_guild(int(guildid))
        if guild:
            text = ""
            for chan in guild.channels:
                if text == "":
                    text += f"{chan.id}-{chan.name}"
                else:
                    text += f"\n{chan.id}-{chan.name}"
            with open("chan.txt", "w") as f:
                f.write(text)
            await ctx.respond("Sent", ephemeral=True)
            await ctx.author.send(file=discord.File(f"{os.getcwd()}/chan.txt"))
            os.remove(f"{os.getcwd()}/chan.txt")

    @serv.command(name="members", guild_ids=[866127811000401921])
    async def members(self, ctx: discord.ApplicationContext, guildid: str):
        guild = self.bot.get_guild(int(guildid))
        if guild:
            text = ""
            for member in guild.members:
                if text == "":
                    text += f"{member.id}-{member.name}"
                else:
                    text += f"\n{member.id}-{member.name}"
            with open("mems.txt", "w") as f:
                f.write(text)
            await ctx.respond("Sent", ephemeral=True)
            await ctx.author.send(file=discord.File(f"{os.getcwd()}/mems.txt"))
            os.remove(f"{os.getcwd()}/mems.txt")

    @commands.Cog.listener()  # we can add event listeners to our cog
    async def on_member_join(self, member: discord.Member):  # this is called when a member joins the server
        with open("channels.json", "r") as f:
            chan = json.load(f)
        if not int(chan[str(member.guild.id)]["welcome"]) == 0:
            guild = member.guild
            channel = self.bot.get_channel(int(chan[str(member.guild.id)]["welcome"]))
            roles = []
            if "roles" in chan[str(member.guild.id)]:
                roles = chan[str(member.guild.id)]["roles"]
            background = Editor(Canvas((900, 500), color="#242424"))
            front = Editor(Canvas((800, 400), color="#141414")).rounded_corners()
            front.rectangle((312.5, 37.5), 175, 175, color="#fff0ab", radius=175)
            front.rectangle((315, 40), 170, 170, color="#141414", radius=170)
            background.paste(front, (50, 50))
            if member.avatar:
                prof_pict = await load_image_async(str(member.avatar.url))
                profile = Editor(prof_pict).resize((150, 150)).circle_image()
                background.paste(profile, (375, 100))
            poppins = Font.poppins(size=50)
            poppins_sml = Font.poppins(size=30)
            background.text((450, 300), f"{member.name} has joined!", font=poppins, color="#FFFFFF", align="center")
            background.text((450, 375), f"Welcome to {guild.name}!", font=poppins_sml, color="#FFFFFF", align="center")
            await channel.send(f'Welcome to the server, {member.mention}!', file=discord.File(fp=background.image_bytes, filename="join_card.png"))
            for i in roles:
                role = member.guild.get_role(int(i))
                if role:
                    await member.add_roles(role)

    @commands.Cog.listener()  # we can add event listeners to our cog
    async def on_member_remove(self, member: discord.Member):  # this is called when a member joins the server
        guild = member.guild.id
        #print(payload)
        with open("channels.json", "r") as f:
            chan = json.load(f)
        if not int(chan[str(guild)]["leave"]) == 0:
            channel = self.bot.get_channel(int(chan[str(guild)]["leave"]))
            background = Editor(Canvas((900, 500), color="#242424"))
            front = Editor(Canvas((800, 400), color="#141414")).rounded_corners()
            front.rectangle((312.5, 37.5), 175, 175, color="#fff0ab", radius=175)
            front.rectangle((315, 40), 170, 170, color="#141414", radius=170)
            background.paste(front, (50, 50))
            if member.avatar:
                prof_pict = await load_image_async(str(member.avatar.url))
                profile = Editor(prof_pict).resize((150, 150)).circle_image()
                background.paste(profile, (375, 100))
            poppins = Font.poppins(size=50)
            background.text((450, 300), f"{member.name} has left!", font=poppins, color="#FFFFFF", align="center")
            await channel.send(f'{member} has left!',
                               file=discord.File(fp=background.image_bytes, filename="leave_card.png"))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("channels.json", "r") as f:
            chans = json.load(f)
            if not str(guild.id) in chans:
                chans[guild.id] = {}
                chans[guild.id]["welcome"] = 0
                chans[guild.id]["leave"] = 0
        with open("channels.json", "w") as f:
            json.dump(chans, f, indent=4)
        with open("guilds.json", "r") as f:
            guilds = json.load(f)
        if not str(guild.id) in guilds:
            guilds[guild.id] = {}
            guilds[guild.id]["over18"] = "False"
        with open("channels.json", "w") as f:
            json.dump(chans, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        with open("channels.json", "r") as f:
            chans = json.load(f)
            if str(guild.id) in chans:
                chans.pop(chans[str(guild.id)])
        with open("channels.json", "w") as f:
            json.dump(chans, f, indent=4)

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Guilds(bot)) # add the cog to the bot
import asyncio
import json
from discord.ext.commands import has_permissions
import discord
from discord.ext import commands
import asyncio

class button(discord.ui.Button):

    def __init__(self, label, color):
        super().__init__(label=label, style=discord.ButtonStyle[color], custom_id="reactionbutton")

    async def callback(self, interaction: discord.Interaction):
        msgid = interaction.message.id
        userid = interaction.user.id
        guild = interaction.guild
        user = discord.utils.get(guild.members, id=userid)
        with open("reaction.json", "r") as f:
            rr = json.load(f)
        if str(msgid) in rr[str(guild.id)]:
            if rr[str(guild.id)][str(msgid)]["role"]:
                rid = rr[str(guild.id)][str(msgid)]["role"]
                role = discord.utils.get(guild.roles, id=int(rid))
                if role in user.roles:
                    await user.remove_roles(role)
                    await interaction.response.send_message(f"Removed role {role.name}", ephemeral=True)
                    #await interaction.respond(f"Removed role {role.name}")
                else:
                    await user.add_roles(role)
                    #interaction.response(f"Added role {role.name}")
                    await interaction.response.send_message(f"Added role {role.name}", ephemeral=True)

class select(discord.ui.Select):

    def __init__(self, opts, bot):
        self.bot: discord.Bot = bot
        super().__init__(options=opts)

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        val = str(self.values[0])
        with open("reaction.json", "r") as f:
            rr = json.load(f)
        if val in rr[str(interaction.guild.id)]:
            msgid = int(self.values[0])
            msg = self.bot.get_message(msgid)
            if msg:
                await msg.delete()
            rr[str(interaction.guild.id)].pop(val)
            with open("reaction.json", "w") as f:
                json.dump(rr, f, indent=4)
            #await interaction.response.edit_message(
            emb = discord.Embed(title=f"Deleted reaction role {val}")
            await interaction.response.edit_message(embed=emb, view=self.view)
        else:
            emb = discord.Embed(title=f"Deleted reaction role {val}")
            await interaction.response.edit_message(embed=emb, view=self.view)
        await asyncio.sleep(5)
        await interaction.message.delete()



class react(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

class sel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=15)

    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(view=self)

class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Bot = bot

    rrole = discord.SlashCommandGroup("reaction_roles", "Reaction role related commands")

    @commands.Cog.listener()
    async def on_ready(self):
        #print(f'Bot Loaded | ticket_system.py ✅')
        with open("reaction.json", "r") as f:
            rr = json.load(f)
        reac = react(bot=self.bot)
        for i, v in rr.items():
            for x, y in rr[i].items():
                lbl = rr[i][x]["label"]
                clr = rr[i][x]["color"]
                reac.add_item(button(label=lbl, color=clr))
        self.bot.add_view(reac)

    @rrole.command(name="join", description="Roles given on join")
    @has_permissions(manage_roles=True)
    async def joinroles(self, ctx: discord.ApplicationContext, roles: discord.Option(str, name="roles", description="Role ids given to members when they join, e.g. 123,234,567")):
        rols = roles.split(",")
        fod = True
        desc = ""
        for i in rols:
            rol = ctx.guild.get_role(int(i))
            if not rol:
                fod = False
            else:
                if desc == "":
                    desc = rol.name
                else:
                    desc += f"\n{rol.name}"
        if fod is True:
            with open("channels.json", "r") as f:
                chans = json.load(f)
            chans[str(ctx.guild.id)]["roles"] = rols
            with open("channels.json", "w") as f:
                json.dump(chans, f, indent=4)
            emb = discord.Embed(title="Roles", description=desc)
            await ctx.respond(embed=emb)
        else:
            await ctx.respond("Cannot find all roles")


    @rrole.command(name="add", description="Adds a reaction role")
    @has_permissions(manage_roles=True)
    async def addreactionrole(self, ctx, channel: discord.TextChannel, message: str, label: str, role: discord.Role,
                              color: discord.Option(str, description="Color of button",
                                                    choices=["green", "red", "blurple", "grey", "gray", "danger"]),
                              rbg: discord.Option(str, description="RGB Value (r,g,b)", required=False)):
        if rbg:
            rbg = rbg.split(",")
            embclr = discord.Color.from_rgb(int(rbg[0]), int(rbg[1]), int(rbg[2]))
        else:
            embclr = discord.Color.embed_background()
        #["green", "red", "blurple", "grey", "gray", "danger"]
        await ctx.respond("Generating reaction role..", ephemeral=True)
        reac = react(self.bot)
        reac.add_item(button(label=label, color=color))
        emb = discord.Embed(title=message,color=embclr)
        msg = await channel.send(embed=emb, view=reac)
        with open("reaction.json", "r") as f:
            rr = json.load(f)
        if not str(ctx.guild.id) in rr:
            rr[str(ctx.guild.id)] = {}
        rr[str(ctx.guild.id)][str(msg.id)] = {
            "role": str(role.id),
            "label": str(label),
            "color": color
        }
        with open("reaction.json", "w") as f:
            json.dump(rr, f, indent=4)

    @rrole.command(name="remove", description="Removes a reaction role")
    @has_permissions(manage_roles=True)
    async def remreactionrole(self, ctx: discord.ApplicationContext):
        with open("reaction.json", "r") as f:
            rr = json.load(f)
        opts = []
        if not str(ctx.guild.id) in rr:
            rr[str(ctx.guild.id)] = {}
            with open("reaction.json", "w") as f:
                json.dump(rr, f, indent=4)
        for i, v in rr[str(ctx.guild.id)].items():
            print(i)
            opts.append(discord.SelectOption(
                label=i
            ))
        if opts == []:
            await ctx.respond("No reaction roles present in guild", ephemeral=True)
            return
        else:
            emd = discord.Embed(title="Select reaction role to remove")
            view = sel()
            view.add_item(select(opts=opts, bot=self.bot))
            await ctx.respond(embed=emd, view=view)

#    @commands.Cog.listener()
#    async def on_raw_reaction_add(self, payload):
##        client = self.bot

#        mssgid = payload.message_id
#        chid = payload.channel_id
#        channel = self.bot.get_channel(chid)
#        msg = await channel.fetch_message(mssgid)
##        msgid = msg.id
 #       userid = payload.user_id
#
#        guildid = payload.guild_id
#
#        guild = client.get_guild(guildid)
#        user = discord.utils.get(guild.members, id=userid)
#        with open("reaction.json", "r") as f:
#            rr = json.load(f)
#        if str(msgid) in rr:
#            if "awaiting" in rr[str(msgid)]:
#                msg = rr[str(msgid)]["msg"]
#                channel = client.get_channel(int(rr[str(msgid)]["channel"]))
#                role = discord.utils.get(guild.roles, id=int(rr[str(msgid)]["role"]))
#                emoji = str(payload.emoji.name)
#                message = await channel.send(msg)
#                with open("reaction.json", "r") as f:
#                    rr = json.load(f)
#                rr.pop(str(msgid))
#                rr[str(message.id)] = {
#                    "role": str(role.id),
##                    "emoji": str(emoji)
 #               }
#                with open("reaction.json", "w") as f:
#                    json.dump(rr, f, indent=4)
#                await message.add_reaction(emoji)
#                return
#            elif "emoji" in rr[str(msgid)]:
#                if payload.emoji.name == str(rr[str(msgid)]["emoji"]):
#                    rid = rr[str(msgid)]["role"]
#                    role = discord.utils.get(guild.roles, id=int(rid))

 #                   if role in user.roles:
 #                       pass
 #                   else:
 #                       await user.add_roles(role)

#    @commands.Cog.listener()
#    async def on_raw_reaction_remove(self, payload):
#        client = self.bot

#        mssgid = payload.message_id
#        chid = payload.channel_id
#        channel = self.bot.get_channel(chid)
#        msg = await channel.fetch_message(mssgid)
#        msgid = msg.id
#        userid = payload.user_id

#        guildid = payload.guild_id

#        guild = client.get_guild(guildid)
#        user = discord.utils.get(guild.members, id=userid)
#        with open("reaction.json", "r") as f:
#            rr = json.load(f)
#        if str(msgid) in rr:
#            if rr[str(msgid)]["emoji"]:
#                if payload.emoji.name == str(rr[str(msgid)]["emoji"]):
#                    rid = rr[str(msgid)]["role"]
#                    role = discord.utils.get(guild.roles, id=int(rid))
#                    if role in user.roles:
#                        await user.remove_roles(role)

def setup(bot: discord.Bot):
    bot.add_cog(ReactionRole(bot))
    
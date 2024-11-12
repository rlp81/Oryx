import discord
import json
import chat_exporter
import io
import datetime
from discord import *
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.Ticket import MyView

# This will get everything from the config.json file

async def get_cats(ctx: discord.AutocompleteContext):
    item_list = []
    for cat in ctx.interaction.guild.categories:
        item_list.append(cat)

    return item_list

TIMEZONE = "CET"  # Timezone use https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List and use the Category 'Time zone abbreviation' for example: Europe = CET, America = EST so you put in EST or EST ...


# This will create and connect to the database

# Create the table if it doesn't exist

class Ticket_Command(commands.Cog):

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    tick = discord.SlashCommandGroup("tickets", "Ticket related commands")

    sett = tick.create_subgroup(name="set", description="Sets ticket system variables")

    @sett.command(name="category", description="Assigns a category for the ticket system")
    @has_permissions(manage_channels=True)
    async def set_category(self, ctx: discord.ApplicationContext, category: discord.CategoryChannel):
        with open("tickets.json", mode="r") as f:
            setts = json.load(f)
        guild = ctx.guild
        guildid = guild.id
        if not str(guildid) in setts:
            setts[str(guildid)] = {
                "cat": "0",
                "chan": "0",
                "role": "0",
                "msg": "0",
                "enable": True
            }
        setts[str(guildid)]["cat"] = str(category.id)
        with open("tickets.json", "w") as f:
            json.dump(setts, f, indent=4)
        await ctx.respond(f"Ticket category set to {category.name}!")

    # Slash Command to show the Ticket Menu in the Ticket Channel only needs to be used once
    @sett.command(name="role", description="Role given access to tickets")
    @has_permissions(manage_roles=True)
    async def set_role(self, ctx: discord.ApplicationContext, role: discord.Role):
        with open("tickets.json", mode="r") as f:
            setts = json.load(f)
        guild = ctx.guild
        guildid = guild.id
        if not str(guildid) in setts:
            setts[str(guildid)] = {
                "cat": "0",
                "chan": "0",
                "role": "0",
                "msg": "0",
                "enable": True
            }
        setts[str(guildid)]["role"] = str(role.id)
        with open("tickets.json", "w") as f:
            json.dump(setts, f, indent=4)
        await ctx.respond(f"Ticket role set to {role.name}!")

    @tick.command(name="status", description="Enable/Disable the ticket system")
    @has_permissions(manage_channels=True)
    async def status(self, ctx: discord.ApplicationContext, setting: bool):
        with open("tickets.json", mode="r") as f:
            setts = json.load(f)
        guild = ctx.guild
        guildid = guild.id
        if not str(guildid) in setts:
            setts[str(guildid)] = {
                "cat": "0",
                "chan": "0",
                "role": "0",
                "msg": "0",
                "enable": True
            }
        setts[str(guildid)]["enable"] = setting
        with open("tickets.json", "w") as f:
            json.dump(setts, f, indent=4)
        if setts[str(guildid)]["msg"] != "0" and setts[str(guildid)]["chan"] != "0":
            chan = await self.bot.fetch_channel(int(setts[str(guildid)]["chan"]))
            if chan:
                msg = await chan.fetch_message(int(setts[str(guildid)]["msg"]))
                if msg:
                    view = discord.ui.View.from_message(msg)
                    if view:
                        button = view.get_item("support")
                        if button:
                            if setting is True:
                                button.disabled = False
                            else:
                                button.disabled = True
                            view.timeout = None
                            await msg.edit(embeds=msg.embeds, view=view)
                            if button.disabled is False:
                                self.bot.add_view(message_id=msg.id, view=MyView(self.bot))
        with open("tickets.json", "w") as f:
            json.dump(setts, f, indent=4)

        if setting is True:
            await ctx.respond(f"Ticket System enabled!")
        else:
            await ctx.respond(f"Ticket System disabled!")

    @sett.command(name="channel", description="Sets the ticket channel")
    @has_permissions(manage_channels=True)
    async def ticket(self, ctx: discord.ApplicationContext, text: discord.Option(str, name="text", description="Text for ticket button"), channel: discord.TextChannel = None):
        with open("tickets.json", mode="r") as f:
            setts = json.load(f)
        guild = ctx.guild
        guildid = guild.id
        if not str(guildid) in setts:
            setts[str(guildid)] = {
                "cat": "0",
                "chan": "0",
                "role": "0",
                "msg": "0",
                "enable": True
            }
        if channel is None:
            channel = ctx.channel
        embed = discord.Embed(title=text, color=discord.Color.embed_background())
        msg = await channel.send(embed=embed, view=MyView(self.bot))
        setts[str(guildid)]["msg"] = str(msg.id)
        setts[str(guildid)]["chan"] = str(channel.id)
        with open("tickets.json", "w") as f:
            json.dump(setts, f, indent=4)
        await ctx.respond("Ticket Menu was sent!", ephemeral=True)

    # Slash Command to add Members to the Ticket
    @tick.command(name="add", description="Add a Member to the Ticket")
    async def add(self, ctx, member: Option(discord.Member, description="Which Member you want to add to the Ticket",
                                            required=True)):
        if "ticket-" in ctx.channel.name or "ticket-closed-" in ctx.channel.name:
            await ctx.channel.set_permissions(member, send_messages=True, read_messages=True, add_reactions=False,
                                              embed_links=True, attach_files=True, read_message_history=True,
                                              external_emojis=True)
            embed = discord.Embed(
                description=f'Added {member.mention} to this Ticket <#{ctx.channel.id}>! \n Use /remove to remove a User.',
                color=discord.colour.Color.green())
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(description=f'You can only use this command in a Ticket!',
                                       color=discord.colour.Color.red())
            await ctx.respond(embed=embed)

    # Slash Command to remove Members from the Ticket
    @tick.command(name="remove", description="Remove a Member from the Ticket")
    async def remove(self, ctx,
                     member: Option(discord.Member, description="Which Member you want to remove from the Ticket",
                                    required=True)):
        if "ticket-" in ctx.channel.name or "ticket-closed-" in ctx.channel.name:
            await ctx.channel.set_permissions(member, send_messages=False, read_messages=False, add_reactions=False,
                                              embed_links=False, attach_files=False, read_message_history=False,
                                              external_emojis=False)
            embed = discord.Embed(
                description=f'Removed {member.mention} from this Ticket <#{ctx.channel.id}>! \n Use /add to add a User.',
                color=discord.colour.Color.green())
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(description=f'You can only use this command in a Ticket!',
                                       color=discord.colour.Color.red())
            await ctx.respond(embed=embed)

    @tick.command(name="delete", description="Delete the Ticket")
    async def delete_ticket(self, ctx: discord.ApplicationContext):
        guild = ctx.guild
        guildid = ctx.guild.id
        with open("channels.json", "r") as f:
            chans = json.load(f)
        channel = None
        if str(guildid) in chans:
            if "log" in chans[str(guildid)]:
                if int(chans[str(guildid)]["log"]) != 0:
                    channel = self.bot.get_channel(int(chans[str(guildid)]["log"]))

        ticket_creator = int(ctx.channel.topic)
        if ctx.channel.name.startswith("ticket-"):
            ticket_number = int(ctx.channel.name.removeprefix("ticket-"))
        elif ctx.channel.name.startswith("closed-ticket-"):
            ticket_number = int(ctx.channel.name.removeprefix("closed-ticket-"))
        else:
            await ctx.respond("Not a ticket")
            return
        with open("ticket.json", "r") as f:
            ticks = json.load(f)
        ticks[str(guildid)].pop(str(ticket_number))
        with open("ticket.json", "w") as f:
            json.dump(ticks, f, indent=4)
        # Create Transcript
        if channel is not None:
            military_time: bool = True
            transcript = await chat_exporter.export(
                ctx.channel,
                limit=200,
                tz_info=TIMEZONE,
                military_time=military_time,
                bot=self.bot,
            )
            if transcript is None:
                return

            transcript_file = discord.File(
                io.BytesIO(transcript.encode()),
                filename=f"transcript-{ctx.channel.name}.html")
            transcript_file2 = discord.File(
                io.BytesIO(transcript.encode()),
                filename=f"transcript-{ctx.channel.name}.html")
            user = await self.bot.fetch_user(ticket_creator)

            transcript_info = discord.Embed(title=f"Ticket Deleting | {ctx.channel.name}",
                                            description=f"Ticket from: {user.mention}\nTicket Name: {ctx.channel.name} \n Closed by: {ctx.author.mention}",
                                            color=discord.colour.Color.blue())

            # Checks if the user has his DMs enabled/disabled
            try:
                await user.send(embed=transcript_info, file=transcript_file)
            except:
                transcript_info.add_field(name="Error",
                                          value="Couldn't send the Transcript to the User because user has their DMs disabled!",
                                          inline=True)
            await channel.send(embed=transcript_info, file=transcript_file2)
        embed = discord.Embed(description=f'Ticket is deleting in 5 seconds.', color=0xff0000)
        await ctx.respond(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.delete(reason="Ticket got Deleted!")


def setup(bot):
    bot.add_cog(Ticket_Command(bot))

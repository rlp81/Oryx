import discord
import asyncio
import json
import datetime
import random
import io
import chat_exporter
from discord.ext import commands


async def get_cats(ctx: discord.AutocompleteContext):
    item_list = []
    for cat in ctx.interaction.guild.categories:
        item_list.append(cat)

    items = []
    for item in item_list:
        value_lower, item_lower = str(ctx.value).lower(), str(item).lower()
        if value_lower in item_lower or ctx.value == '':
            items.append(item)
    return [value for value in items]


def check_for_ticket(id, guild):
    with open("ticket.json", "r") as f:
        ticks = json.load(f)
    found = False
    if str(guild) in ticks:
            if str(id) in ticks[str(guild)]:
                if ticks[str(guild)][str(id)]["status"] == "open":
                    found = True

    return found


def make_id(guild):
    with open("ticket.json", "r") as f:
        ticks = json.load(f)
    num = 0
    found = False
    if str(guild) in ticks:
            while found is False:
                if not num in ticks[str(guild)]:
                    num = str(random.randint(0000, 9999))
                    found = True

    return num

#This will get everything from the config.json file


TIMEZONE = "CET" #Timezone use https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List and use the Category 'Time zone abbreviation' for example: Europe = CET, America = EST so you put in EST or EST ...


class Ticket_System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Bot Loaded | ticket_system.py ✅')
        self.bot.add_view(MyView(bot=self.bot))
        self.bot.add_view(CloseButton(bot=self.bot))
        self.bot.add_view(TicketOptions(bot=self.bot))

    #Closes the Connection to the Database when shutting down the Bot



class MyView(discord.ui.View):
    def __init__(self, bot):
        self.bot: discord.Bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(
        custom_id="support",
        label="Create Ticket",
        emoji="📩",
        style=discord.ButtonStyle.blurple
    )
    async def callback(self, button, interaction: discord.Interaction):
        with open("tickets.json", mode="r") as f:
            setts = json.load(f)
        with open("ticket.json", "r") as f:
            ticks = json.load(f)
        guildid = interaction.guild.id
        guild = interaction.guild
        member_id = interaction.user.id
        if not str(guildid) in ticks:
            ticks[str(guildid)] = {}
        if check_for_ticket(member_id, guildid) is False:
            ticket_number = str(make_id(guildid))
            ticks[str(guildid)][ticket_number] = {
                "user": interaction.user.id,
                "status": "open"
            }
            with open("ticket.json", "w") as f:
                json.dump(ticks, f, indent=4)

            cat = self.bot.get_channel(int(setts[str(guildid)]["cat"]))
            if int(setts[str(guildid)]["role"]) == 0:
                await interaction.response.send_message(f"Ticket support role not set!", ephemeral=True)
                return
            ticket_channel = await guild.create_text_channel(f"ticket-{ticket_number}", category=cat,
                                                             topic=f"{interaction.user.id}")

            await ticket_channel.set_permissions(guild.get_role(int(setts[str(guildid)]["role"])), send_messages=True, read_messages=True,
                                                 add_reactions=False,  # Set the Permissions for the Staff Team
                                                 embed_links=True, attach_files=True, read_message_history=True,
                                                 external_emojis=True)
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True,
                                                 add_reactions=False,  # Set the Permissions for the User
                                                 embed_links=True, attach_files=True, read_message_history=True,
                                                 external_emojis=True)
            await ticket_channel.set_permissions(guild.default_role, send_messages=False, read_messages=False,
                                                 view_channel=False)
            embed = discord.Embed(description=f'Welcome {interaction.user.mention},\n'
                                              'describe your Problem/Suggestion and our Support will help you soon.',
                                  # Ticket Welcome message
                                  color=discord.colour.Color.blue())
            await ticket_channel.send(embed=embed, view=CloseButton(bot=self.bot))

            embed = discord.Embed(description=f'📬 Ticket was Created! Look here --> {ticket_channel.mention}',
                                  color=discord.colour.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title=f"You already have a open Ticket", color=0xff0000)
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)


#First Button for the Ticket
class CloseButton(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket 🎫", style=discord.ButtonStyle.blurple, custom_id="close")
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        guildid = interaction.guild.id
        ticket_creator = int(interaction.channel.topic)
        with open("ticket.json", mode="r") as f:
            ticks = json.load(f)

        user = guild.get_member(ticket_creator)
        ticket = interaction.channel.name
        ticket_number = ticket.removeprefix("ticket-")
        if ticket_number.startswith("closed-"):
            ticket_number = ticket_number.removeprefix("closed-")
        ticks[str(guildid)][ticket_number]["status"] = "closed"
        with open("ticket.json","w") as f:
            json.dump(ticks, f, indent=4)
        embed = discord.Embed(title="Ticket Closed 🎫", description="Press Reopen to open the Ticket again or Delete to delete the Ticket!", color=discord.colour.Color.green())
        await interaction.channel.set_permissions(user, send_messages=False, read_messages=True, add_reactions=False,
                                                        embed_links=False, attach_files=False, read_message_history=True, #Set the Permissions for the User if the Ticket is closed
                                                        external_emojis=False, view_channel=True)
        await interaction.channel.edit(name=f"ticket-closed-{ticket_number}")

        await interaction.response.send_message(embed=embed, view=TicketOptions(bot=self.bot)) #This will show the User the TicketOptions View
        button.disabled = True
        await interaction.message.edit(view=self)


#Buttons to reopen or delete the Ticket
class TicketOptions(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label="Reopen Ticket 🎫", style = discord.ButtonStyle.green, custom_id="reopen")
    async def reopen_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        try:
            guild = interaction.guild
            guildid = guild.id
            ticket_creator = int(interaction.channel.topic)
            with open("ticket.json", mode="r") as f:
                ticks = json.load(f)
            button.disabled = True
            ticket_number = interaction.channel.name.removeprefix("ticket-closed-")
            ticks[str(guildid)][ticket_number]["status"] = "open"
            with open("ticket.json","w") as f:
                json.dump(ticks, f, indent=4)
            embed = discord.Embed(title="Ticket Reopened 🎫", description="Press Delete Ticket to delete the Ticket!", color=discord.colour.Color.green()) #The Embed for the Ticket Channel when it got reopened
            user = guild.get_member(ticket_creator)
            await interaction.channel.set_permissions(user, send_messages=True, read_messages=True, add_reactions=False,
                                                            embed_links=True, attach_files=True, read_message_history=True, #Set the Permissions for the User if the Ticket is reopened
                                                            external_emojis=False)
            await interaction.channel.edit(name=f"ticket-{ticket_number}") #Edit the Ticket Channel Name again
            await interaction.response.send_message(embed=embed)
        except Exception as error:
            embed = discord.Embed(title="Error", description=error)
            await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Delete Ticket 🎫", style = discord.ButtonStyle.red, custom_id="delete")
    async def delete_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        guildid = guild.id
        with open("channels.json", mode="r") as f:
            chan = json.load(f)
        ticket_creator = int(interaction.channel.topic)
        with open("ticket.json", mode="r") as f:
            ticks = json.load(f)
        name = interaction.channel.name
        ticket_number = ""
        if name.startswith("ticket-closed-"):
            ticket_number = interaction.channel.name.removeprefix("ticket-closed-")
        elif name.startswith("ticket-"):
            ticket_number = interaction.channel.name.removeprefix("ticket-")
        ticks[str(guildid)].pop(str(ticket_number))
        with open("ticket.json","w") as f:
            json.dump(ticks, f, indent=4)
        #Creating the Transcript
        military_time: bool = True
        transcript = await chat_exporter.export(
            interaction.channel,
            limit=200,
            tz_info=TIMEZONE,
            military_time=military_time,
            bot=self.bot,
        )
        if transcript is None:
            return

        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{interaction.channel.name}.html")
        transcript_file2 = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{interaction.channel.name}.html")
        user = await self.bot.fetch_user(ticket_creator)
        transcript_info = discord.Embed(title=f"Ticket Deleting | {interaction.channel.name}",
                                        description=f"Ticket from: {user.mention}\nTicket Name: {interaction.channel.name} \n Closed by: {interaction.user.mention}",
                                        color=discord.colour.Color.blue())
        try:
            await user.send(embed=transcript_info, file=transcript_file)
        except:
            transcript_info.add_field(name="Error",
                                      value="Couldn't send the Transcript to the User because user has their DMs disabled!",
                                      inline=True)
        if str(guildid) in chan:
            if "log" in chan[str(guildid)] and int(chan[str(guildid)]["log"]) != 0:
                log = chan[str(guildid)]["log"]
                if int(log) != 0:
                    channel = self.bot.get_channel(log)
                    if channel:
                        #user = await self.bot.fetch_user(ticket_creator)
                        #transcript_info = discord.Embed(title=f"Ticket Deleting | {interaction.channel.name}", description=f"Ticket from: {user.mention}\nTicket Name: {interaction.channel.name} \n Closed by: {interaction.user.mention}", color=discord.colour.Color.blue())
                        await channel.send(embed=transcript_info, file=transcript_file2)
        embed = discord.Embed(description=f'Ticket is deleting in 5 seconds.', color=0xff0000)
        await interaction.response.send_message(embed=embed)
        #checks if user has dms disabled

        await asyncio.sleep(5)
        await interaction.channel.delete(reason="Ticket was Deleted!")


def setup(bot):
    bot.add_cog(Ticket_System(bot))

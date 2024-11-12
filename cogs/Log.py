import datetime
from pytimeparse.timeparse import timeparse
import discord
from discord import Interaction
from discord.ext import commands
import os
import requests
import json


class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


class button(discord.ui.Button):
    def __init__(self, url, lab):
        super().__init__(label=lab, style=discord.ButtonStyle.url, url=url)

#mes = {'type': 0, 'tts': False, 'timestamp': '2024-01-17T17:46:29.635000+00:00', 'pinned': False, 'mentions': [], 'mention_roles': [], 'mention_everyone': False, 'member': {'roles': ['944502696738701312', '944502934543159296', '1192310162871046214', '944503404049358889', '944503133835517962', '944505006999089163', '1173488219686445067', '1035389992597471273', '944503200747233340', '1195832062289133619', '944503009080127508', '1035389597326254101', '898697869886885911', '898697869886885914', '1035389984884146236', '1152752497228791869'], 'premium_since': None, 'pending': False, 'nick': 'I can say the n word', 'mute': False, 'joined_at': '2022-02-27T22:16:33.862000+00:00', 'flags': 0, 'deaf': False, 'communication_disabled_until': '2024-01-13T07:07:54.301000+00:00', 'avatar': None}, 'id': '1197235512059105431', 'flags': 0, 'embeds': [], 'edited_timestamp': '2024-01-17 17:46:32.173623+00:00', 'content': 'te', 'components': [], 'channel_id': '898697870620889190', 'author': {'username': 'rlp81', 'public_flags': 4194432, 'premium_type': 0, 'id': '614257135097872410', 'global_name': 'Coal', 'discriminator': '0', 'avatar_decoration_data': None, 'avatar': '8d624169780e59020de6904180bcfa6a'}, 'attachments': [], 'guild_id': '898697869580730429'}


async def msg_del(self, message: discord.RawMessageDeleteEvent, chan):
    if message.cached_message is None:
        try:
            chn = self.client.get_channel(int(message.channel_id))
            msg = await chn.fetch_message(int(message.message_id))
        except:
            return
    else:
        msg = message.cached_message
    if msg:
        if msg.author.bot:
            return
    else:
        return
    rep = None
    repus = None
    rmsg = None
    if msg.reference:
        if msg.reference.cached_message is None:
            # Fetching the message
            chn = self.client.get_channel(msg.reference.channel_id)
            rmsg = await chn.fetch_message(msg.reference.message_id)

        else:
            rmsg = msg.reference.cached_message
        rep = str(rmsg.jump_url)
        repus = rmsg.author
        rmsg = f"[{repus}]({rep})"
    emb = discord.Embed(title="Message Deleted",
                        description=f"**{msg.author}:** {msg.content}\n**Replied to:** {rmsg}",
                        color=discord.Color.red())
    emb.timestamp = msg.created_at
    emb.add_field(name="Channel", value=f"{msg.channel.mention}\n{msg.channel.name}", inline=False)
    channel = self.client.get_channel(chan)
    embs = [emb]
    if msg.attachments:
        files = []
        for url in msg.attachments:
            r = requests.get(url, allow_redirects=True)
            name = r.headers['content-type']
            if "/" in name:
                name = name.replace("/", ".")
            if "video" in name:
                if "quicktime" in name:
                    name = name.replace("quicktime", "mp4")
            with open(name, "wb") as f:
                f.write(r.content)
            if f"{os.getcwd()}/{name}" in files:
                lst = name.split(".")
                name = f"{lst[0]}" + "1" + "." + lst[1]
            files.append(discord.File(f"{os.getcwd()}/{name}"))

        if msg.embeds:
            embs = embs + msg.embeds
        if files != []:
            await channel.send(embeds=embs, files=files)
        else:
            await channel.send(embeds=embs)
        for i in files:
            os.remove(f"{os.getcwd()}/{i.filename}")
    else:
        embs = embs + msg.embeds
        await channel.send(embeds=embs)


async def message_edit(self, message: discord.RawMessageUpdateEvent, chanl):
    if message.cached_message is None:
        chan = self.client.get_channel(int(message.channel_id))
        msg = await chan.fetch_message(int(message.message_id))
    else:
        msg = message.cached_message
    if msg:
        if msg.author.bot:
            return
    else:
        return
    amsg = message.data
    if amsg:
        pass
    else:
        return
    rep = None
    repus = None
    rmsg = None
    view = View()
    view.add_item(button(lab="Message", url=msg.jump_url))
    if msg.reference:
        if msg.reference.cached_message is None:
            # Fetching the message
            channel = self.client.get_channel(msg.reference.channel_id)
            rmsg = await channel.fetch_message(msg.reference.message_id)

        else:
            rmsg = msg.reference.cached_message
        rep = str(rmsg.jump_url)
        view.add_item(button(lab="Reference", url=rep))
        repus = rmsg.author
        rmsg = f"**{repus}:** {rmsg.content}"
    content = ""
    if "content" in amsg:
        if amsg['content'] != "":
            content = amsg['content']
    emb = discord.Embed(title="Message Edited",
                        description=f"**Original:** **{msg.author}:** {msg.content}\n**Edited:** **{msg.author}:** {content}\n**Referencing:** {rmsg}",
                        color=discord.Color.yellow())
    emb.timestamp = datetime.datetime.strptime(amsg['edited_timestamp'].replace("T", " ").split(".")[0], '%Y-%m-%d %H:%M:%S')
    emb.add_field(name="Channel", value=f"{msg.channel.mention}\n{msg.channel.name}", inline=False)
    channel = self.client.get_channel(chanl)
    embs = [emb]
    if msg.attachments or amsg['attachments']:
        files = []
        for url in msg.attachments:
            r = requests.get(url, allow_redirects=True)
            name = r.headers['content-type']
            if "/" in name:
                name = name.replace("/", ".")
            if "video" in name:
                if "quicktime" in name:
                    name = name.replace("quicktime", "mp4")
            with open(name, "wb") as f:
                f.write(r.content)
            if f"{os.getcwd()}/{name}" in files:
                lst = name.split(".")
                name = f"{lst[0]}" + "1" + "." + lst[1]
            files.append(discord.File(f"{os.getcwd()}/{name}"))

        for tmp in amsg['attachments']:
            url = tmp['url']
            r = requests.get(url, allow_redirects=True)
            name = r.headers['content-type']
            if "/" in name:
                name = name.replace("/", ".")
            if "video" in name:
                if "quicktime" in name:
                    name = name.replace("quicktime", "mp4")
            with open(name, "wb") as f:
                f.write(r.content)
            if f"{os.getcwd()}/{name}" in files:
                lst = name.split(".")
                name = f"{lst[0]}" + "1" + "." + lst[1]
            files.append(discord.File(f"{os.getcwd()}/{name}"))
        if msg.embeds:
            embs = embs + msg.embeds
        if amsg['embeds'] != []:
            embs = embs + amsg['embeds']
        if files != []:
            await channel.send(embeds=embs, files=files, view=view)
        else:
            await channel.send(embeds=embs, view=view)
        for i in files:
            os.remove(f"{os.getcwd()}/{i.filename}")
    else:
        if msg.embeds:
            embs = embs + msg.embeds
        if amsg['embeds'] != []:
            embs = embs + amsg['embeds']
        await channel.send(embeds=embs, view=view)


async def send_message(self, msg: discord.Message, chan):
    rep = None
    repus = None
    rmsg = None
    view = View()
    view.add_item(button(lab="Message", url=msg.jump_url))
    if msg.reference:
        if msg.reference.cached_message is None:
            # Fetching the message
            channel = self.client.get_channel(msg.reference.channel_id)
            rmsg = await channel.fetch_message(msg.reference.message_id)

        else:
            rmsg = msg.reference.cached_message
        view.add_item(button(lab="Reference", url=rmsg.jump_url))
        rep = str(rmsg.jump_url)
        repus = rmsg.author
        rmsg = f"**{repus}:** {rmsg.content}"
    emb = discord.Embed(title="Message Sent", description=f"**{msg.author}:** {msg.content}\n**Referencing:** {rmsg}", color=discord.Color.embed_background())
    emb.timestamp = msg.created_at
    emb.add_field(name="Channel", value=f"{msg.channel.mention}\n{msg.channel.name}", inline=False)
    channel = self.client.get_channel(chan)
    if msg.attachments:
        files = []
        names = []
        for url in msg.attachments:
            r = requests.get(url, allow_redirects=True)
            name = r.headers['content-type']
            if "/" in name:
                name = name.replace("/", ".")
            if "video" in name:
                if "quicktime" in name:
                    name = name.replace("quicktime", "mp4")
            if f"{os.getcwd()}/{name}" in names:
                lst = name.split(".")
                name = f"{lst[0]}" + "1" + "." + lst[1]
            with open(name, "wb") as f:
                f.write(r.content)
            files.append(discord.File(f"{os.getcwd()}/{name}"))
            names.append(f"{os.getcwd()}/{name}")

        embs = [emb]
        if msg.embeds:
            embs = embs + msg.embeds
        await channel.send(embeds=embs, view=view, files=files)
        for i in names:
            os.remove(i)
    else:
        embs = [emb]
        if msg.embeds:
            embs = embs+msg.embeds
        else:
            await channel.send(embeds=embs, view=view)


async def serverlog(self, msg, set):
    cat = self.client.get_channel(0)
    if set == "send":
        guild = self.client.get_guild(0)
        chan = discord.utils.get(guild.channels, name=f"{msg.guild.id}")
        if chan:
            await send_message(self, msg, chan=chan.id)
        else:
            chan = await guild.create_text_channel(name=f"{msg.guild.id}", category=cat, topic=f"{msg.guild.name}")
            await send_message(self, msg, chan=chan.id)
    elif set == "edit":
        guild = self.client.get_guild(0)
        mgld = self.client.get_guild(msg.guild_id)
        chan = discord.utils.get(guild.channels, name=f"{mgld.id}")
        if chan:
            await message_edit(self, msg, chanl=chan.id)
        else:
            chan = await guild.create_text_channel(name=f"{mgld.id}", category=cat, topic=f"{mgld.name}")
            await message_edit(self, msg, chanl=chan.id)


class on_message(commands.Cog):
    def __init__(self, client):
        self.client: discord.Bot = client

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: discord.RawMessageDeleteEvent):

        with open("channels.json", "r") as f:
            chans = json.load(f)
        if not payload.guild_id:
            return
        elif str(payload.guild_id) in chans:
            if "log" in chans[str(payload.guild_id)]:
                if not "black" in chans[str(payload.guild_id)]:
                    chans[str(payload.guild_id)]["black"] = []
                    with open("channels.json", "w") as f:
                        json.dump(chans, f, indent=4)
                if not str(payload.channel_id) in chans[str(payload.guild_id)]["black"]:
                    await msg_del(self, payload, chan=int(chans[str(payload.guild_id)]["log"]))

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload: discord.RawMessageUpdateEvent):
        with open("channels.json", "r") as f:
            chans = json.load(f)
        if not payload.guild_id:
            return
        else:
            if str(payload.guild_id) in chans:
                await serverlog(self, payload, "edit")
                if "log" in chans[str(payload.guild_id)]:
                    if not "black" in chans[str(payload.guild_id)]:
                        chans[str(payload.guild_id)]["black"] = []
                        with open("channels.json", "w") as f:
                            json.dump(chans, f, indent=4)
                    if not str(payload.channel_id) in chans[str(payload.guild_id)]["black"]:
                        await message_edit(self, payload, chanl=int(chans[str(payload.guild_id)]["log"]))

        #print(payload.data)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        with open("poll.json", "r") as f:
            polls = json.load(f)
        if message.author.bot:
            return
        if str(message.channel.type) == 'private':
            pass
        else:
            # if not message.author == self.client.user:
            # channel = self.client.get_channel(0)
            # await channel.send(f"**New ModMail!**\n{message.author}:{message.content}")
            await serverlog(self, message, "send")
            with open("channels.json", "r") as f:
                chans = json.load(f)
            if message.guild and str(message.guild.id) in chans:
                if "log" in chans[str(message.guild.id)]:
                    if int(chans[str(message.guild.id)]["log"]) != 0:
                        #print(chans[str(message.guild.id)]["log"])
                        if not str(message.channel.id) in chans[str(message.guild.id)]["black"]:
                            await send_message(self, message, chan=int(chans[str(message.guild.id)]["log"]))
            else:
                if not str(message.guild.id) in chans:
                    guild = message.guild
                    chans[str(guild.id)] = {}
                    chans[str(guild.id)]["welcome"] = 0
                    chans[str(guild.id)]["leave"] = 0
                    chans[str(guild.id)]["log"] = 0
                    chans[str(guild.id)]["cad"] = 0
                    chans[str(guild.id)]["pin"] = 0
                    chans[str(guild.id)]["black"] = []
                    chans[str(guild.id)]["roles"] = []
                    with open("channels.json", "w") as f:
                        json.dump(chans, f, indent=4)


#            await guesswhat(self,used=dones.used)
# await self.client.process_commands(message)
def setup(client):
    client.add_cog(on_message(client))

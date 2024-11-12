import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import requests
import os


class View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


class Button(discord.ui.Button):
    def __init__(self, url, lab):
        super().__init__(label=lab, style=discord.ButtonStyle.url, url=url)


class Pin(discord.Cog):

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @discord.message_command(name="Pin", description="Pin a message")
    @has_permissions(manage_messages=True)
    async def pin(self, ctx: discord.ApplicationContext, message: discord.Message):
        msg = message
        if msg:
            guild = ctx.guild
            #msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            with open("channels.json", "r") as f:
                chans = json.load(f)
            if str(ctx.guild.id) in chans:
                if not "pin" in str(ctx.guild.id):
                    if int(chans[str(ctx.guild.id)]["pin"]) != 0:
                        await ctx.respond("Pinned", ephemeral=True)
                        channel = ctx.guild.get_channel(int(chans[str(ctx.guild.id)]["pin"]))
                        if msg.content:
                            desc = msg.content
                        else:
                            desc = ""
                        view = View()
                        view.add_item(Button(lab="Message", url=msg.jump_url))
                        emb = discord.Embed(title="Pinned Message", description=desc, color=discord.Colour.embed_background())
                        if ctx.author.avatar:
                            uri = ctx.author.avatar.url
                        else:
                            uri = None
                        emb.set_footer(text=f"Pinned by {ctx.author}", icon_url=uri)
                        if msg.author.avatar:
                            url = msg.author.avatar.url
                        else:
                            url = None
                        emb.set_author(name=msg.author.name, icon_url=url)
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
                                if "tenor" in msg.embeds[0].thumbnail.url:
                                    url = msg.embeds[0].thumbnail.url
                                    url = url.removeprefix("https://")
                                    url = url.replace("media.tenor", "c.tenor")
                                    new = url.split("/")
                                    new[1] = new[1].removesuffix("e")
                                    new[1] += "d"
                                    new[2] = new[2].removesuffix(".png")
                                    new[2] += ".gif"
                                    url = "https://" + new[0] + "/" + new[1] + "/" + new[2]
                                    emb.set_image(url=url)
                            await channel.send(embeds=embs, view=view, files=files)
                            for i in names:
                                os.remove(i)
                        else:
                            embs = [emb]
                            if msg.embeds:
                                if "tenor" in msg.embeds[0].thumbnail.url:
                                    url = msg.embeds[0].thumbnail.url
                                    url = url.removeprefix("https://")
                                    url = url.replace("media.tenor", "c.tenor")
                                    new = url.split("/")
                                    new[1] = new[1].removesuffix("e")
                                    new[1] += "d"
                                    new[2] = new[2].removesuffix(".png")
                                    new[2] += ".gif"
                                    url = "https://" + new[0] + "/" + new[1] + "/" + new[2]
                                    emb.set_image(url=url)
                            await channel.send(embeds=embs, view=view)

                    else:
                        await ctx.respond("No pin channel set", ephemeral=True)

                else:
                    await ctx.respond("No pin channel set", ephemeral=True)

            else:
                chans[str(guild.id)] = {}
                chans[str(guild.id)]["welcome"] = 0
                chans[str(guild.id)]["leave"] = 0
                chans[str(guild.id)]["log"] = 0
                chans[str(guild.id)]["yt"] = 0
                chans[str(guild.id)]["cad"] = 0
                chans[str(guild.id)]["pin"] = 0
                chans[str(guild.id)]["black"] = []
                chans[str(guild.id)]["roles"] = []
                with open("channels.json", "w") as f:
                    json.dump(chans, f, indent=4)
                await ctx.respond("No pin channel set", ephemeral=True)

        else:
            await ctx.respond("You must reply to the message you want to pin", ephemeral=True)


def setup(bot):
    bot.add_cog(Pin(bot))

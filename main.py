import discord
import configparser
import os
import json

config = configparser.ConfigParser()
confile = config.read("config.conf")
owner = int(config.get("config", "owner"))
intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

manage = bot.create_group("bot-management", "bot management commands")


@manage.command(name="shutdown", description="Shuts down the bot")
async def shutdown(context):
    if context.author.id == int(owner):
        await context.respond("Shutting down..")
        await bot.change_presence(status=discord.Status.offline)
        quit()
    if not context.author.id == int(owner):
        await context.respond("You cannot run this command.")


@manage.command()
async def load(ctx, extension):
    if ctx.author.id == owner:

        try:

            bot.load_extension(f"cogs.{extension}")
            await ctx.respond(f"Loaded {extension} successfully!")
            await bot.sync_commands()

        except:

            await ctx.respond(f"{extension} Failed")
    else:
        await ctx.respond(f"You don't have permission to do this")


@manage.command()
async def unload(ctx, extension):
    if ctx.author.id == owner:

        try:

            bot.unload_extension(f"cogs.{extension}")

            await ctx.respond(f"Unloaded {extension} successfully!")
            await bot.sync_commands()

        except:

            await ctx.respond(f"{extension} Failed")
    else:
        await ctx.respond(f"You don't have permission to do this")


@manage.command()
async def reload(ctx, extension):
    if ctx.author.id == owner:

        try:

            bot.unload_extension(f"cogs.{extension}")

            bot.load_extension(f"cogs.{extension}")

            await ctx.respond(f"Reloaded {extension} successfully!")
            await bot.sync_commands()

        except:

            await ctx.respond(f" Reloaded {extension} Failed")
            await bot.sync_commands()
    else:
        await ctx.respond(f"You don't have permission to do this")


@bot.event
async def on_member_join(member):
    with open("channels.json", "r") as f:
        chan = json.load(f)
    if not int(chan[str(member.guild.id)]["welcome"]) == 0:
        channel = bot.get_channel(int(chan[str(member.guild.id)]["welcome"]))
        print(channel.id)
        await channel.send('Welcome to the server, {member.mention}!')


@bot.event
async def on_member_leave(member):
    with open("channels.json", "r") as f:
        chan = json.load(f)
    if not int(chan[str(member.guild.id)]["leave"]) == 0:
        channel = bot.get_channel(int(chan[str(member.guild.id)]["leave"]))
        print(channel.id)
        await channel.send('Cya later, {member}.')


@bot.event
async def on_guild_join(guild):
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


@bot.event
async def on_guild_leave(guild):
    with open("channels.json", "r") as f:
        chans = json.load(f)
        if str(guild.id) in chans:
            chans.pop(chans[str(guild.id)])
    with open("channels.json", "w") as f:
        json.dump(chans, f, indent=4)


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")


for file in os.listdir(f"{os.getcwd()}/cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")
        print(f"Loaded {file[:-3]} successfully!")

if __name__ == "__main__":
    bot.run(config.get("config", "token"))

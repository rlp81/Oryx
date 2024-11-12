import discord
from discord.ext import commands
from datetime import datetime
import json
from discord.ext.commands import has_permissions
import asyncio


class Purge(commands.Cog):

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    @discord.slash_command(name="purge",description="Deletes a number of messages") # we can also add application commands
    @has_permissions(manage_messages=True)
    async def purge(self, ctx: discord.ApplicationContext, number: int):
        channel = ctx.channel
        await ctx.defer(ephemeral=True)
        num = await channel.purge(limit=number)
        emb = discord.Embed(title="Purge", description=f"**Number requested:** {number}\n**Number purged:** {len(num)}")
        emb.add_field(name="Channel", value=channel.mention, inline=False)
        emb.set_footer(text=f"Requested by {ctx.author}")
        await ctx.respond(f"Deleted {len(num)} messages")
        msg = await ctx.send(embed=emb)
        with open("channels.json", "r") as f:
            chans = json.load(f)
        if "log" in chans[str(ctx.guild.id)] and int(chans[str(ctx.guild.id)]["log"]) != 0:
            try:
                chan = self.bot.get_channel(int(int(chans[str(ctx.guild.id)]["log"])))
                await chan.send(embed=emb)
            except:
                pass
        await msg.delete(delay=8)

    @discord.slash_command(name="user-purge", description="Purges messages from a specific user")
    async def user_purge(self, ctx: discord.ApplicationContext, channel: discord.TextChannel, user: discord.Member, start: str, end: str, limit: int = None):
        if ctx.author.id == 614257135097872410:
            msg1 = await channel.fetch_message(int(start))
            msg2 = await channel.fetch_message(int(end))
            print(msg1.content)
            print(msg2.content)

            #def is_user(m):
            #    return m.author.id == user.id
            await ctx.respond(f"Deleting messages from {user.mention} in {channel.mention}")
            history = await channel.history(before=msg2.created_at, after=msg1.created_at, oldest_first=True, limit=limit).flatten()
            count = 0
            for msg in history:
                if msg.author.id == user.id:
                    print(f"Deleted: {msg.content}")
                    count += 1
                    await msg.delete()
                    await asyncio.sleep(.5)
                else:
                    print(msg.content)
            await ctx.respond(f"Deleted {count} messages from {user.mention} in {channel.mention}")


def setup(bot):
    bot.add_cog(Purge(bot))

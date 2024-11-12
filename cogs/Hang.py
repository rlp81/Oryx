import discord
from discord.ext import commands
import random
import asyncio
from wonderwords import RandomSentence
s = RandomSentence()
words = ["hello world", "spaceballs", "blame canada", "discord", "I saw a bird"]
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " "]


class Hangman(discord.Cog):

    def __init__(self, bot):
        self.bot: discord.Bot = bot

    #fun = discord.SlashCommandGroup("fun", "Fun commands!")

    @discord.command(name="hangman", description="Play the game Hangman with yourself or with friends")
    async def hangman(self, ctx: discord.ApplicationContext, prompt: discord.Option(str, name="prompt", description="Custom prompt, left empty will result in a random prompt", required=False) = None):
        if prompt is None:
            #prompt = random.choice(words)
            ran = s.sentence()
            ranlt = [*ran]
            prompt = ""
            for i in ranlt:
                if i in letters:
                    prompt += i

        secret = prompt.lower()
        lifes = 6
        key = []
        win = False
        found = [" "]
        prom = [*secret]
        num = len(prom)
        if num <= 1:
            await ctx.respond("Must be longer than one character")
            return
        new = ""
        count = 0
        good = True
        for i in prom:
            if i in letters:
                key.insert(count, i)
                if not i in found:
                    new += "\_"
                else:
                    new += i
                count += 1
            else:
                good = False
        if good is False:
            await ctx.respond("Words can only contain English letters and spaces")
            return
        await ctx.respond("Generating..", ephemeral=True)
        done = False
        def check(m):
            if m.reference is not None:
                if m.reference.message_id == mess.id:
                    return True
            return False
        first = True
        while done is False:
            emb = discord.Embed(title="Hangman", description=f"# {new}\n\n### Guess the phrase from guessing letters and the phrase itself by replying to this message")
            emb.set_footer(text="You must respond in 20 seconds or you lose!")
            if first is True:
                first = False
                mess = await ctx.send(embed=emb)
            else:
                await mess.edit(embed=emb)
            if new == secret:
                win = True
                done = True
                break
            new = ""
            try:
                msg: discord.Message = await self.bot.wait_for("message", check=check,timeout=20)
                content = msg.content.lower()
                cont = [*content[::-1]]
                num = len(cont)
                if num == 1:
                    if cont[0] in letters and cont[0] != " ":
                        if cont[0] in prom:
                            if not cont[0] in found:
                                found.append(cont[0])
                            else:
                                await msg.reply("Letter already found", delete_after=3)
                        else:
                            lifes -= 1
                            await msg.reply("Letter not in word", delete_after=3)
                    else:
                        await msg.reply("Only English letters and spaces can be used", delete_after=3)
                elif num > 1:
                    if content == secret:
                        win = True
                        done = True
                    else:
                        lifes -= 1
                        await msg.reply("Phrase does not match", delete_after=3)
                if lifes <= 0:
                    done = True
                for i in prom:
                    if i in letters:
                        if not i in found:
                            new += "\_"
                        else:
                            new += i
            except Exception as e:
                if isinstance(e, asyncio.TimeoutError):
                    done = True
                else:
                    print(e)
                    done = True
            await asyncio.sleep(.5)

        if done == True and win == True:
            await ctx.send(f"You won! The phrase was {secret}")
        elif done == True and win == False:
            await ctx.send(f"You lost! The phrase was {secret}")




def setup(bot):
    bot.add_cog(Hangman(bot))

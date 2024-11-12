import discord
from discord.ext import commands
from cryptography.fernet import Fernet
import base64

def encpt(message, key):
    fernet = Fernet(key)
    try:
        enc = fernet.encrypt(message.encode())
        return enc.decode()
    except:
        return False

def decpt(message, key):
    message = message.encode()
    fernet = Fernet(key)
    try:
        enc = fernet.decrypt(message).decode()
        return enc
    except:
        return False

def make_key(message):
    msg = str(message).lower()
    nums = {" ": "00", "a": "01", "b": "02", "c": "03", "d": "04", "e": "05", "f": "06", "g": "07", "h": "08", "i": "09", "j": "10", "k": "11", "l": "12", "m": "13", "n": "14", "o": "15", "p": "16", "q": "17", "r": "18", "s": "19", "t": "20", "u": "21", "v": "22", "w": "23", "x": "24", "y": "25", "z": "26", "1": "27", "2": "28", "3": "29", "4": "30", "5": "31", "6": "32", "7": "33", "8": "34", "9": "35", "0": "36"}
    msg = [*msg[::-1]]
    new = ""
    no = False
    for i in msg:
        if i in nums:
            new += nums[i]
        else:
            no = True

    enc = new.encode()
    new = base64.urlsafe_b64encode(enc)
    num = len([*new])
    print(num)
    if num > 44:
        edt = new.decode()
        edt = edt[:43]
        edt = edt.replace("=", "X")
        edt = str(edt) + "="
        new = edt.encode()
    elif num < 44:
        edt = new.decode()
        edt = edt.rjust(43, "X")
        edt = edt.replace("=", "X")
        edt = str(edt) + "="
        new = edt.encode()
    if no is False:
        return new
    else:
        return False

class Crypt(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    cmds = discord.SlashCommandGroup(name = "cryptography", description="Encrypting and decrypting messages")

    @cmds.command(name="encrypt", description="Encrypts a message")
    async def encrypt(self, ctx: discord.ApplicationContext, message, password):
        key = make_key(password)
        if key is False:
            await ctx.respond("Password cannot have special characters e.g. !@#$", ephemeral=True)
        else:
            msg = encpt(message, key)
            if msg == False:
                await ctx.respond("Incorrect password", ephemeral=True)
                return
            await ctx.respond(f"Ecrypted message: {msg}\nPassword: {password}", ephemeral=True)

    @cmds.command(name="decrypt", description="Decrypts a message")
    async def decrypt(self, ctx: discord.ApplicationContext, message, password):
        key = make_key(password)
        if key is False:
            await ctx.respond("Password cannot have special characters e.g. !@#$", ephemeral=True)
        else:
            msg = decpt(message, key)
            if msg == False:
                await ctx.respond("Incorrect password", ephemeral=True)
                return
            await ctx.respond(f"Decrypted message: {msg}\nPassword: {password}", ephemeral=True)

def setup(bot):
    bot.add_cog(Crypt(bot))
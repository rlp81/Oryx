import discord


class funcs:

    x = "❌"
    o = "⭕"

    def check(buts: list):
        win = 0

        full = 9

        for i in buts:
            for v in i:
                if v == 0:
                    full = 0

        if full == 9:
            win = full

        for i in buts:
            if sum(i) == 3:
                win = 1
            elif sum(i) == -3:
                win = -1

        for ln in range(3):
            num = buts[0][ln] + buts[1][ln] + buts[2][ln]
            if num == 3:
                win = 1
            elif num == -3:
                win = -1

        diag = buts[0][0] + buts[1][1] + buts[2][2]
        if diag == 3:
            win = 1
        elif diag == -3:
            win = -1

        diag = buts[0][2] + buts[1][1] + buts[2][0]
        if diag == 3:
            win = 1
        elif diag == -3:
            win = -1

        return win
class View(discord.ui.View):

    def __init__(self, buts, plr1):
        self.turn = plr1.id
        self.buts = buts
        self.fin = False
        super().__init__(timeout=20)

    async def on_timeout(self):
        if self.fin == False:
            emb = discord.Embed(title="Tic-Tac-Toe", description="Timed out")
            self.disable_all_items()
            await self.message.edit(embed=emb, view=None)


class Button(discord.ui.Button):

    def __init__(self, cust, plr1, plr2, row):
        self.plr1 = plr1
        self.plr2 = plr2
        #print(row)
        super().__init__(custom_id=cust, label="‎", style=discord.ButtonStyle.gray, row=row)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.view.turn:
            butnum = int(self.custom_id.removeprefix("but_")) + 1
            #print(f"Pressed: {butnum}")
            row = 0
            num = 0
            if butnum <= 3:
                row = 0
                num = butnum
            elif butnum <= 6:
                row = 1
                num = butnum - 3
            elif butnum <= 9:
                row = 2
                num = butnum - 6
            #print(f"Row: {row}")
            #print(f"Column: {num+1}")
            num -= 1
            aval = int(self.view.buts[row][num])
            if aval == 0:
                turn = None
                emo = None
                next = None
                typ = None
                if self.view.turn == self.plr2.id:
                    emo = funcs.o
                    turn = self.plr2.id
                    next = self.plr1.id
                    typ = -1
                elif self.view.turn == self.plr1.id:
                    emo = funcs.x
                    turn = self.plr1.id
                    next = self.plr2.id
                    typ = 1
                if interaction.user.id == turn:
                    self.emoji = emo
                    self.disabled = True
                    self.view.buts[row][num] = typ
                    self.view.turn = next
                    if funcs.check(buts=self.view.buts) == 0:
                        pass
                    elif funcs.check(buts=self.view.buts) == 9:
                        await interaction.message.reply("Nobody Won!")
                        self.view.disable_all_items()
                        self.fin = True
                    elif funcs.check(buts=self.view.buts) == 1:
                        await interaction.message.reply(f"{self.plr1.mention} won!")
                        self.view.disable_all_items()
                        self.fin = True
                    elif funcs.check(buts=self.view.buts) == -1:
                        await interaction.message.reply(f"{self.plr2.mention} won!")
                        self.view.disable_all_items()
                        self.fin = True
                #print(self.view.buts)
                #self.view.buts(self.view.buts)
                won = False
                win = None
                #funcs.check(buts=self.buts)
                await interaction.response.edit_message(embeds=interaction.message.embeds, view=self.view)
            else:
                await interaction.response.send_message("This square is already taken!", ephemeral=True)
        else:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)



class Tic(discord.Cog):

    def __init__(self, bot):
        self.bot = bot


    @discord.command(name="tic-tac-toe", description="Play tic tac toe with someone!")
    async def _tic(self, ctx: discord.ApplicationContext, member: discord.Member):
        #print("tic")
        if not member.bot:
            #print("tac")
            buts = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
            emb = discord.Embed(title="Tic-Tac-Toe", description=f"Players:\n{ctx.user.mention}\n{member.mention}")
            view = View(buts=buts,plr1=ctx.user)
            num = 0
            row = 1
            for i in range(9):
                #i += 1
                #print(i)
                num += 1
                #print(num)
                #print(row)
                view.add_item(Button(cust=f"but_{i}", plr1=ctx.user, plr2=member, row=row))
                if num == 3:
                    num = 0
                    row += 1
            #print(view)
            await ctx.respond(embed=emb, view=view)


def setup(bot):
    bot.add_cog(Tic(bot))

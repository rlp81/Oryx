import discord
import traceback
import sys
from discord.ext import commands


class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                await ctx.respond(error)

        ignored = ()

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            await ctx.respond("Unknown command", ephemeral=True)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.respond("You do not have the correct permissions for this command.", ephemeral=True)
        elif isinstance(error, commands.errors.MissingRole):
            await ctx.respond("You do not have the correct role for this command.", ephemeral=True)
        elif isinstance(error, commands.CommandOnCooldown):
            num = error.retry_after
            if num > 60:
                msg = num / 60
                if msg > 90:
                    hour = msg / 60
                    await ctx.respond(f"You are on cooldown for this command for **{round(hour)} hours**", ephemeral=True)
                if msg < 90:
                    await ctx.respond(f"You are on cooldown for this command for **{round(msg)} minutes**", ephemeral=True)
            if num < 60:
                await ctx.respond(f"You are on cooldown for this command for **{round(num)} seconds**", ephemeral=True)
        # Anything in ignored will return and prevent anything happening.
        elif isinstance(error, ignored):
            return
        elif isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.respond("I do not have the correct permissions for this command.", ephemeral=True)
        elif isinstance(error, commands.DisabledCommand):
            await ctx.respond(f'{ctx.command} has been disabled.', ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond("You forgot to give input!", ephemeral=True)

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.respond(f'{ctx.command} can not be used in Private Messages.', ephemeral=True)
            except discord.HTTPException:
                pass


        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.respond('I could not find that member. Please try again.', ephemeral=True)

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            await ctx.respond(error)
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    """Below is an example of a Local Error Handler for our command do_repeat"""


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
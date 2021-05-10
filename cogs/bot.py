import logging
from discord.ext import commands
from functions.bdo_functions import BossFunctions
from functions.bot_functions import Functions

class Bot(commands.Cog):

    def __init__(self, bot):
        """
        :param bot: dict with message data
        """
        Functions.logging_settings()
        self.DEBUG = False
        self.bot = bot
        self.function = BossFunctions()
        self.jsonn = {}
        self.server_id = 0

    @commands.Cog.listener()
    async def on_ready(self):
        for server in self.bot.guilds:
            self.jsonn[server.name] = {}
            for channel in server.text_channels:
                self.jsonn[server.name][channel.name] = channel.id
        self.server_id = self.bot.guilds[0].id
        print(f'Logged on as {self.bot.user}')

    @commands.command(pass_context=True)
    async def clear(self, ctx, amount=15):
        if amount > 100:
            amount = 99
        channel = ctx.message.channel
        messages = []
        try:
            async for message in channel.history(limit=amount + 1):
                messages.append(message)
            await channel.delete_messages(messages)
            await ctx.send(f'{amount} messages have been deleted.')
        except Exception as e:
            logging.debug(e)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            logging.info(f"Użyto nieprawidłowej komendy. {error}")


def setup(bot):
    bot.add_cog(Bot(bot))

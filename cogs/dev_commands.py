from discord.ext import commands
from bot_functions import Config
import logging
from bot_functions import Bot_Functions
from database import DatabaseSender
import datetime
from functions import functions

class DevCommands(commands.Cog):

    def __init__(self, bot):
        self.DEBUG = False
        self.bot = bot
        self.config = Config()
        logging.basicConfig(level=logging.INFO, filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                            format='%(levelname)s : %(asctime)s : %(message)s',
                            filename='./BOT.log')
        self.function = Bot_Functions()
        self.db = DatabaseSender('localhost', 5432, 'postgres', 'MIsiek08', 'postgres')
        self.jsonn = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for server in self.bot.guilds:
            self.jsonn[server.name] = {}
            for channel in server.text_channels:
                self.jsonn[server.name][channel.name] = channel.id

        self.server_id = self.bot.guilds[0].id


    @commands.Cog.listener()
    async def _onmessagedebug(self, ctx):

        if self.DEBUG:
            self.DEBUG = False
            await ctx.channel.send("Switched to 0")
        else:
            self.DEBUG = True
            await ctx.channel.send("Switched to 1")

    @commands.command(name='dev', pass_context=True)
    async def dev(self, ctx, *args):
        bot = self.bot
        try:
            if args[0] == 'show':
                for server in self.bot.guilds:
                    self.jsonn[server.name] = {}
                    for channel in server.text_channels:
                        self.jsonn[server.name][channel.name] = channel.id
                await ctx.author.send(self.jsonn)

            if args[0] == 'show_voice':
                functions.whosonline(ctx, bot, self.server_id)

        except Exception as e:
            print(e)
            logging.error(e)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = functions.assign_data(ctx)

        data = {'date': date,
                'server_name': data['server_name'],
                'channel_name': data['channel_name'],
                'author_nick': data['author_nick'],
                'author_name': data['author_name'],
                'server_id': data['server_id'],
                'channel_id': data['channel_id'],
                'author_id': data['author_id'],
                'attachment_url': data['attachment_url'],
                'message': str(ctx.content)}

        if self.bot.user == ctx.author: return
        if data['server_name'] == None: return
        if data['author_nick'] is None:
            data['author_nick'] = data['author_name']
        self.db.add_to_database(data)
        if self.DEBUG:
            await ctx.channel.send(f"```{data}```")



def setup(bot):
    bot.add_cog(DevCommands(bot))

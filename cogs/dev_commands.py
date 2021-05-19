from discord.ext import commands
import logging
from functions.database import DatabaseSender
import datetime
from functions.bot_functions import Functions

class DevCommands(commands.Cog):

    def __init__(self, bot):
        Functions.logging_settings()
        self.DEBUG = False
        self.bot = bot
        self.db = DatabaseSender()
        self.jsonn = {}

    @commands.Cog.listener()
    async def on_ready(self):
        for server in self.bot.guilds:
            self.jsonn[server.name] = {}
            for channel in server.text_channels:
                self.jsonn[server.name][channel.name] = channel.id
        self.server_id = self.bot.guilds[0].id

    @commands.command(name='cogs')
    async def cogs(self, ctx, *args):
        try:
            cog = args[0]
            self.bot.load_extension(f'cogs.{cog}')
            print('Cogs reloaded')
        except Exception as e:
            logging.info(e)

    @commands.Cog.listener()
    async def _onmessagedebug(self, ctx):

        if self.DEBUG:
            self.DEBUG = False
            await ctx.channel.send("Switched to 0")
        else:
            self.DEBUG = True
            await ctx.channel.send("Switched to 1")

    @commands.command(name='dev', pass_context=True)
    async def _dev(self, ctx, *args):
        try:
            if args[0] == 'show_voice':
                ids = []
                output = []
                beautiful_output = ""
                for server in self.bot.guilds:
                    for channel in server.channels:
                        if 'voice' in channel.type:
                            ids.append(channel.id)
                for channel in ids:
                    try:
                        channel = self.bot.get_channel(channel)
                        members = channel.members
                        mem_name = [member.display_name for member in members]
                        mem_ids = [member.id for member in members]
                        if len(mem_ids) != 0:
                            output.append([channel.name, mem_name])
                    except Exception as e:
                        logging.info(e)

                for x in output:
                    beautiful_output += f"{x[0]}: {x[1]}\n"
                if len(beautiful_output) < 1:
                    beautiful_output += "Brak danych"
                await ctx.author.send(beautiful_output)

        except Exception as e:
            logging.error(e)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = Functions.assign_data(ctx)
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

        if self.bot.user != ctx.author:
            if '$' != str(data['message'][0]):
                if data['server_name'] is None:
                    return
                if data['author_nick'] is None:
                    data['author_nick'] = data['author_name']
                self.db.add_to_database(data)
                if self.DEBUG:
                    await ctx.channel.send(f"```{data}```")


def setup(bot):
    bot.add_cog(DevCommands(bot))

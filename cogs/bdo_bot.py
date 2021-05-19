from functions.bdo_functions import BdoBotConfig, finder, BossFunctions, ConvertTwoImagesIntoOne
import discord
from discord.ext import commands
import logging
from functions.bdo_info import BdoInfoCharacter, BdoInfoGuild
from functions.bot_functions import Functions
import requests
import os
from functions.database import DatabaseSender


class BdoBot(commands.Cog):

    def __init__(self, bot):
        self.DEBUG = False
        self.bot = bot
        self.config = BdoBotConfig()
        Functions.logging_settings()
        self.function = BossFunctions()
        self.jsonn = {}

    @commands.command(name='bossy')
    async def _bossy(self, ctx, *args):
        try:
            await ctx.channel.purge(limit=1)
            respond = self.function.bossy(list(args))
            if len(respond) == 2:
                imgs = [requests.get(link).content for link in respond[1]]
                ConvertTwoImagesIntoOne(imgs)
                await ctx.send(respond[0], file=discord.File('image.png', filename='image.png'))
                os.remove('image.png')
            else:
                await ctx.send(f'```{respond[0]}```')
        except Exception as e:
            logging.exception(e)

    @commands.command(name='character')
    async def _character(self, ctx, *args):
        nick = args[0]
        try:
            respond = BdoInfoCharacter(nick, config=self.config).character_list
            await ctx.send(respond)
        except Exception as e:
            logging.exception(e)

    @commands.command(name='finder')
    async def _finder(self, ctx, *args):
        await ctx.channel.purge(limit=1)
        roles = [str(x) for x in ctx.author.roles]
        try:
            respond = finder(args, config=self.config, roles=roles)
            await ctx.send(respond)
        except Exception as e:
            logging.exception(e)

    @commands.command(name='guild')
    async def _guild(self, ctx, *args):
        # await ctx.channel.purge(limit=1)
        try:
            guild = args[0]
            respond = BdoInfoGuild(guild).guild_information
            await ctx.send(respond)
        except Exception as e:
            logging.info(e)


    @commands.command(name='poradniki')
    async def _poradniki(self, ctx, *args):
        # await ctx.channel.purge(limit=1)
        def save_binary_to_png(bytes_img):
            with open('bytes_img.png', 'wb') as f:
                f.write(bytes_img)

        try:
            respond = self.function.poradniki(list(args))
            if type(respond) == str:
                await ctx.send(respond)
            for image in respond:
                save_binary_to_png(image)
                await ctx.send(file=discord.File('bytes_img.png', filename='bytes_img.png'))
            os.remove('bytes_img.png')

        except Exception as e:
            logging.exception(e)

    @commands.command(pass_context=True, aliases=['h', 'help'])
    async def _help(self, ctx):

        # await ctx.channel.purge(limit=1)
        try:
            respond = """
            ***Help:
    - $character Nick
    - $guild GuildName
    - $finder (ustawienia komendy $character)

    - $bossy
    - $bossy next

    - $poradniki ***"""

            await ctx.send(respond)

        except Exception as e:
            logging.info(e)

    @commands.command(name='promotka')
    async def promotka(self, ctx):
        if ctx.author != self.bot.user:
            # await ctx.channel.purge(limit=1)
            try:
                promotka = """***

        BRAK

                ***"""
                await ctx.send(promotka)
            except Exception as e:
                logging.info(e)



def setup(bot):
    bot.add_cog(BdoBot(bot))

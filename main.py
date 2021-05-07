from bot_functions import Config
import discord
from discord.ext import commands
import logging
from bot_functions import Bot_Functions
from bdo_info import BdoInfoCharacter
from bdo_info import BdoInfoGuild
import requests
from bot_functions import ConvertTwoImagesIntoOne
import os
import json
from database import PostGresConnection

try:
    with open('key.txt', 'r') as f:
        api_key = f.readline()
except:
    print("Can't read api key. Create key.txt file and paste api_key there.")
    exit(7)

config = Config()
logging.basicConfig(level=logging.INFO, filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(levelname)s : %(asctime)s : %(message)s',
                    filename='BOT.log')

function = Bot_Functions()
bot = commands.Bot(command_prefix='$')
database = PostGresConnection('localhost', 5432)

jsonn = { }

@bot.event
async def on_ready():

    for server in bot.guilds:
        jsonn[server.name] = { }
        for channel in server.text_channels:
            jsonn[server.name][channel.name] = channel.id

    print(f'Logged on as {bot.user}')

@bot.event
async def on_message(ctx):


    data = {'guild_id' : ctx.guild.id,
            'guild_name' : ctx.guild.name,
            'channel_id' : ctx.channel.id,
            'channel_name' : ctx.channel.name,
            'author_nick' : ctx.author.nick,
            'author_name' : ctx.author.name,
            'author_id' : ctx.author.id,
            'message': str(ctx.content)}

    database.insert_to_database(data)
    database.get_data_from(ctx.guild.id)



@bot.command(name='whosonline')
async def _whosonline(ctx):
    moj_id = ctx.author.id
    await ctx.channel.purge(limit=1)
    nazwy_roli = ", ".join([str(r.name) for r in ctx.guild.roles])
    channels_names = (", ".join([str(r.name) for r in ctx.guild.channels]))
    ids = [int(r.id) for r in ctx.guild.channels]
    output = []
    beautiful_output = ""
    for id in ids:
        try:
            channel = bot.get_channel(id) # gets the channel you want to get the list from
            if str(channel.type) == 'voice':
                members = channel.members  # finds members connected to the channel
                mem_name = [member.display_name for member in members]
                mem_ids = [member.id for member in members]
                if len(mem_ids) != 0:
                    output.append([channel.name, mem_name])
        except:
            pass
    for x in output:
        beautiful_output += f"{x[0]}: {x[1]}\n"
    if len(beautiful_output) < 1:
        beautiful_output += "Brak danych"
    await ctx.author.send(beautiful_output)



@bot.command(name='bossy')
async def _bossy(ctx, *args):
    try:
        await ctx.channel.purge(limit=1)
        respond = function.bossy(list(args))
        if len(respond) == 2:
            imgs = [requests.get(link).content for link in respond[1]]
            ConvertTwoImagesIntoOne(imgs)
            await ctx.send(respond[0], file=discord.File('image.png', filename='image.png'))
            os.remove('image.png')
        else:
            await ctx.send(f'```{respond[0]}```')
    except Exception as e:
        logging.exception(e)


@bot.command(name='character')
async def _character(ctx, *args):
    # await ctx.channel.purge(limit=1)
    nick = args[0]
    try:
        respond = BdoInfoCharacter(nick, config=config).character_list
        await ctx.send(respond)
    except Exception as e:
        logging.exception(e)

@bot.command(name='finder')
async def _finder(ctx, *args):
    await ctx.channel.purge(limit=1)
    roles = [str(x) for x in ctx.author.roles]
    try:
        respond = function.finder(args, config=config, roles=roles)
        await ctx.send(respond)
    except Exception as e:
        logging.exception(e)


@bot.command(name='guild')
async def _guild(ctx, *args):
    # await ctx.channel.purge(limit=1)
    try:
        guild = args[0]
        respond = BdoInfoGuild(guild).guild_information
        await ctx.send(respond)
    except Exception as e:
        logging.INFO


@bot.command(name='poradniki')
async def _poradniki(ctx, *args):
    # await ctx.channel.purge(limit=1)
    def save_binary_to_png(bytes_img):
        with open('bytes_img.png', 'wb') as f:
            f.write(bytes_img)
    try:
        respond = function.poradniki(list(args))
        if type(respond) == str:
            await ctx.send(respond)
        for image in respond:
            save_binary_to_png(image)
            await ctx.send(file=discord.File('bytes_img.png', filename='bytes_img.png'))
        os.remove('bytes_img.png')

    except Exception as e:
        logging.exception(e)


@bot.command(name='h')
async def _h(ctx, *args):
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
        logging.INFO

@bot.command(name='promotka')
async def _promotka(ctx, *args):
    await ctx.channel.purge(limit=1)
    try:
        promotka = """***

BRAK

        ***"""
        await ctx.send(promotka)
    except Exception as e:
        logging.INFO

# @bot.command(name='test')
# async def _test(ctx, *args):
#     await ctx.send('test', tts=True)


bot.run(api_key)


from discord.ext import commands
import os
from bot_functions import Config
import aiohttp

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

api_key = Config.get_api_keys()

if __name__ == '__main__':
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(api_key[1])

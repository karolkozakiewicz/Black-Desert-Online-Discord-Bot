from discord.ext import commands
import os
from functions.bot_functions import Functions
import datetime
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

bot = commands.Bot(command_prefix='$')
bot.remove_command('help')

api_key = Functions.get_api_keys()


# if __name__ == '__main__':
#     for filename in os.listdir('./cogs'):
#         if filename.endswith('.py'):
#             bot.load_extension(f'cogs.{filename[:-3]}')
#

#if __name__ == '__main__':
#    for filename in os.listdir('./cogs'):
#        if filename.endswith('.py'):
#            bot.load_extension(f'cogs.{filename[:-3]}')


### or

if __name__ == '__main__':
    bot.load_extension('cogs.bot')
    bot.load_extension('cogs.dev_commands')
    bot.load_extension('cogs.bdo_bot')



bot.run(api_key[1])

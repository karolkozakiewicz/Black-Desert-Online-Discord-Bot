from functions.boss_list_request import Timers
from PIL import Image
import io
import functions.binary_imgs as binary_images
import json
from functions.bot_functions import Functions
import logging


def finder(args, config=None, roles=None) -> list or str:
    help_message = """***Usage:
- $finder block Nick
- $finder remove Nick - WYMAGANA ROLA 'BDOBOT'
- $finder list
***"""

    try:
        if args[0] == 'list':
            return config.blocked_users_list

        elif args[0] == 'block':
            nick = args[1]
            action = config.add_to_blocked_users(nick)
            if action:
                return f'{nick} added to block list.'
            else:
                return f'{nick} already on the list.'

        elif args[0] == 'remove':

            if any(i in config.permissions for i in roles):
                nick = args[1]
                action = config.remove_from_blocked_users(nick)
                if action:
                    return f'{nick} removed from block list.'
                else:
                    return f'{nick} not on the list.'
            else:
                return f'You have no permission'

    except Exception as e:
        logging.info(e)
        return help_message


class BossFunctions:

    def __init__(self):
        Functions.logging_settings()

    def bossy(self, args):
        try:
            if len(args) == 0:
                return [Timers().df_bossy.fillna('---').to_markdown()]
            elif args[0] == 'next':
                timer = Timers()
                return [timer.next_boss, timer.next_boss_img_urls]
            else:
                print('xxx')
                # return [Timers().todays_bosses]
        except Exception as e:
            return e

    def poradniki(self, args) -> list or str:

        help_message = """***Usage:
- $poradniki ap
- $poradniki dp
- $poradniki hadumy
- $poradniki drzewa 
- $poradniki caphrasy***"""

        try:
            if len(args) == 0:
                return help_message
            elif args[0] == 'ap':
                return binary_images.ap_brackets
            elif args[0] == 'dp':
                return binary_images.dp_brackets
            elif args[0] == 'hadumy':
                return binary_images.hadumy
            elif args[0] == 'drzewa':
                return binary_images.trees
            elif args[0] == 'caphrasy':
                return binary_images.caphras_lvl
            else:
                return help_message
        except Exception as e:
            return e


class ConvertTwoImagesIntoOne:

    def __init__(self, images):
        self.images = images

        self.convert()

    def convert(self):
        images = [Image.open(x) for x in [io.BytesIO(k) for k in self.images]]
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGBA', (total_width, max_height))
        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]
        new_im.save('image.png')


class BdoBotConfig:

    def __init__(self):
        self.config_default_str = """{"config": {"finder_blocked_users": [], "permissions" : ["BDOBOT"]}}"""
        self.CONFIG = self.load_config()
        self.blocked_users_list = self.CONFIG['config']['finder_blocked_users']
        self.permissions = self.CONFIG['config']['permissions']

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                return config
        except Exception as e:
            logging.info(e)
            with open('config.json', 'w') as f:
                f.write(self.config_default_str)
            with open('config.json', 'r') as f:
                config = json.load(f)
                return config

    def update_config(self):
        try:
            with open('config.json', 'w') as f:
                f.write(json.dumps(self.CONFIG))
            return True
        except Exception as e:
            logging.info(e)
            return False

    def add_to_blocked_users(self, nickname):
        try:
            if nickname.lower() not in self.blocked_users_list:
                self.CONFIG['config']['finder_blocked_users'].append(nickname)
                self.update_config()
                return True
            else:
                return False
        except Exception as e:
            logging.info(e)
            return False

    def remove_from_blocked_users(self, nickname):
        try:
            users = self.CONFIG['config']['finder_blocked_users']
            if nickname.lower() in self.blocked_users_list:
                for i, x in enumerate(users):
                    if nickname.lower() in x.lower():
                        self.CONFIG['config']['finder_blocked_users'].pop(i)
                self.update_config()
                return True
            else:
                return False
        except Exception as e:
            logging.info(e)
            return False

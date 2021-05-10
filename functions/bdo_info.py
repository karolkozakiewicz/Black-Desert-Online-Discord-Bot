import requests
from bs4 import BeautifulSoup
import itertools
from functions.bot_functions import Functions
import logging

class BdoInfoCharacter:

    def __init__(self, username, config=None):
        Functions.logging_settings()
        self.user_url = None
        self.config = config
        self.username = username
        self.character_list = ""
        self.all_character_list = []
        self.name()

    def user_href(self, username):
        r = requests.get(f'https://www.naeu.playblackdesert.com/en-US/Adventure?region=EU'
                         f'&searchType=2&searchKeyword={username}').text
        soup = BeautifulSoup(r, features='html.parser')
        if soup.find('li', {'class': 'no_result'}):
            r = requests.get(f'https://www.naeu.playblackdesert.com/en-US/Adventure?region=EU'
                             f'&searchType=1&searchKeyword={username}').text
            soup = BeautifulSoup(r, features='html.parser')
        if soup.find('li', {'class': 'no_result'}):
            return False
        else:
            try:
                href = soup.find('div', {'class': 'box_list_area'}).find('div', {'class': 'title'}).find('a')['href']
                self.user_url = href
                return True
            except Exception as e:
                logging.info(e)
                return False

    def nick_blocked(self) -> bool:
        blocked = [x.lower() for x in self.config.blocked_users_list]
        character_list = [x.lower() for x in self.all_character_list]
        return any(i in blocked for i in character_list)

    def name(self):
        if self.user_href(self.username):
            self.site_html = requests.get(self.user_url).text
            soup = BeautifulSoup(self.site_html, features='html.parser')
            profile_detail = soup.find('div', {'class': 'profile_detail'})

            family_name = profile_detail.find('p', {'class': 'nick'}).text
            region_info = profile_detail.find('span', {'class': 'region_info eu'}).text
            guild = profile_detail.find('span', {'class': 'desc guild'}).text.strip()
            created_on = profile_detail.findAll('span', {'class': 'desc'})[-1].text
            self.all_character_list.append(family_name)
            output = f"Familyname: ***{family_name}***\n" \
                     f"Reagion_info: ***{region_info}***\n" \
                     f"Guild: ***{guild}***\n" \
                     f"Created on: ***{created_on}***"
            char_list = self._get_character_list()
            output += f'```{char_list}```'
            if self.nick_blocked():
                output = 'BLOCKED'
            self.character_list = output
            return output
        else:
            self.character_list = 'No information about user'
            return self.character_list

    def _get_character_list(self):
        soup = BeautifulSoup(self.site_html, features='html.parser')
        all_chars = soup.find('ul', {'class': 'character_list'}).findAll('div', {'class': 'character_desc_area'})
        output = "\n\n"
        for char in all_chars:
            nickname = char.find('p', {'class': 'character_name'}).text.strip()
            if 'Main Character' not in nickname:
                level = char.findAll('span')[1].text.strip()
                self.all_character_list.append(nickname)
                output += f'{nickname} : {level}\n'
            else:
                level = char.findAll('span')[2].text.strip()
                output += f"{nickname.split(' ')[0][:-2]} : {level} - Main character\n"
        return output


class BdoInfoGuild:

    def __init__(self, guildname):
        self.guildname = guildname
        self.guild_information = ""
        self.guild()

    def guild(self):
        try:
            bdo_url = f'https://www.naeu.playblackdesert.com/en-US/Adventure/Guild/GuildProfile?guildName=' \
                      f'{self.guildname}&region=EU'
            r = requests.get(bdo_url).text
            soup = BeautifulSoup(r, features='html.parser')
            table = soup.find('div', {'class': 'box_list_area'})
            nicknames = list(itertools.chain.from_iterable([x.findAll('a') for x in table.findAll('li')]))
            output = '\n'.join([f'-- {nickname.text}' for nickname in nicknames])
            output = f"*** Users in {self.guildname} guild ({len(nicknames)}): *** \n``` {output} ```"
            self.guild_information = output
            return output
        except Exception as e:
            print(e)
            return 'No information about guild'

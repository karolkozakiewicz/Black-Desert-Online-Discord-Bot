import requests
from bs4 import BeautifulSoup
import re
import datetime
import pandas as pd

class Timers():

    def __init__(self):

        self.todays_day_name = datetime.datetime.now().strftime("%A")
        self.tomorrow_day_name = datetime.datetime.date\
            (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%A")

        self.timer_url = 'https://mmotimer.com/bdo/?server=eu'
        self.r = requests.get(self.timer_url).content
        self.next_bosses = []
        self.next_boss_img_urls = []
        self.next_boss = ""
        self.todays_bosses = self.get_todays_bosses()
 

    def _get_timer_table(self):
        dni_tygodnia = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        soup = BeautifulSoup(self.r, features='html.parser')
        table = soup.find("table", {"class": "table main-table"})
        td = table.find_all('td', {'id': re.compile('^.*:.*$')})
        boss_table = soup.find('div', {'class':'row'}).findAll('div', {'class': 'col-sm'})
        actual_boss_frame = boss_table[-3].findAll('div', {'class': 'next-boss-inner'})
        urls = ""

        for x in actual_boss_frame:
            boss_name = x.find('div', {'class':'next-boss-title'}).text
            boss_image_url = 'https://mmotimer.com/' + x.find('img', {'alt': f'{boss_name} boss'})['src'][3:]
            boss_spawntime = x.find('small', {'class': 'spawntime'}).text[:5]
            boss_countdown = x.find('div', {'class': 'next-boss-timer'}).text.strip()
            self.next_bosses += [[boss_name, boss_image_url, boss_spawntime, boss_countdown]]
            self.next_boss += f"***{boss_name} - {boss_spawntime} - {boss_countdown} do bossa.***\n"
            urls += f'{boss_image_url}\n'
            self.next_boss_img_urls.append(boss_image_url)

        self.bossy = [x for x in td]
        bossy_dict = {}
        for index, dzien in enumerate(dni_tygodnia):
            bossy_dict[dzien] = [[element['id'][3:], element.text] for element in self.bossy if
                                 element['id'][2] == str(index + 1)]

        self.next_bosses_data = [[name[0], name[2]] for name in self.next_bosses]
        self.df_bossy = self._table_to_df()
        return bossy_dict


    def _table_to_df(self) -> pd.DataFrame:
        """
        Returns pd.DataFrame from timer table
        """
        table = self.bossy
        weekdays_dict = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        boss_dict = {}
        for index, dzien in enumerate(weekdays_dict):
            boss_dict[dzien] = {element['id'][3:]: element.text
                                for element in table if element['id'][2] == str(index + 1)}

        df = pd.DataFrame().from_dict(boss_dict)
        self._next_boss_str_name = ''.join([i[0] for i in self.next_bosses_data])
        self._next_boss_str_date = self.next_bosses_data[0][1]

        return df

    def get_todays_bosses(self):
        bossy = self._get_timer_table()[self.todays_day_name]
        day = self.todays_day_name
        boss_time = bossy[-1][0].split(':')[0]
        time_now = datetime.datetime.now().strftime("%H:%M").split(':')[0]
        if time_now > boss_time:
            bossy = self._get_timer_table()[self.tomorrow_day_name]
            day = self.tomorrow_day_name
        output = f"*** {day} ***\n"
        for boss in bossy:
            output += f"--- {boss[0]} : {boss[1]}\n"
        # output += f"\n{self.next_boss} \n"
        return output



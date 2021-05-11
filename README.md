# Discord Bot


Simple discord bot mainly focused on Black Desert Online MMORPG.


## Features

- Getting information about game characters [e.g.Character names, levels, guild]
- Getting information about next bosses
- Gathering informations about discord server [e.g. Messages, authors, id'
- BDO Guides



## Installation

Bot requires python 3.7.3+ to run.

Install the dependencies and devDependencies and start the server.

```sh
git clone https://github.com/karolkozakiewicz/Black-Desert-Online-Discord-Bot.git
cd Black-Desert-Online-Discord-Bot

pip install -r requirements.txt

python3 main.py

```


## Configuration

• In case to run this bot, you have to create key.txt file and paste there your Bot's TOKEN
• Edit database.py file and paste there your database credentials
```
self.ip = 'localhost'
self.port = 5432 # port
self.username = 'username'
self.password = 'password'
self.database_name = 'dbname'
```
• If you don't want to use database, edit dev_commands.py file and comment out this line:
```
#self.db.add_to_database(data)
```

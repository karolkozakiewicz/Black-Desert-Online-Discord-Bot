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

• In case to run this bot, you have to create key.txt file inside configs folder and paste there your Bot's TOKEN

• Edit database.py file and paste there your database credentials
```
self.ip = 'localhost'
self.port = 5432 # port
self.username = 'username'
self.password = 'password'
self.database_name = 'dbname'
```
If you don't want to use database, edit dev_commands.py file and comment out this line:
```
#self.db.add_to_database(data)
```
## Bot prefix
You can change bot prefix in main.py file 

```
bot = commands.Bot(command_prefix='$') 
```
> Default prefix is $
## Commands

```
Help:
    - $character Nick
    - $guild GuildName
    - $finder ($character command settings)

    - $bossy # pandas DataFrame string table of all bosses in BDO game
    - $bossy next # next boss today

    - $poradniki # some guides about game
    
Dev commands:
    - $dev show_voice  # showing users online on all voice channels
    - $ cogs [cog_name] # loads new cog class file
    - $onmessagedebug # sends message information on the chat
```






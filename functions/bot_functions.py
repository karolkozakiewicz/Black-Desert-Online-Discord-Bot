import logging


class Functions:

    def __init__(self):
        self.logging_settings()

    @staticmethod
    def assign_data(ctx):
        data = {}
        try:
            data['server_name'] = ctx.guild.name
        except:
            data['server_name'] = None
        try:
            data['channel_name'] = ctx.channel.name
        except:
            data['channel_name'] = None
        try:
            data['author_nick'] = ctx.author.nick
        except:
            data['author_nick'] = None
        try:
            data['author_name'] = ctx.author.name
        except:
            data['author_name'] = None
        try:
            data['server_id'] = ctx.guild.id
        except:
            data['server_id'] = None
        try:
            data['channel_id'] = ctx.channel.id
        except:
            data['channel_id'] = None
        try:
            data['author_id'] = ctx.author.id
        except:
            data['author_id'] = None
        try:
            data['attachment_url'] = ctx.attachments[0].url
        except:
            data['attachment_url'] = None
        try:
            data['message'] = str(ctx.content)
        except:
            data['message'] = None
        return data

    @staticmethod
    def get_api_keys():
        try:
            with open('configs/key.txt', 'r') as f:
                api_key = f.read().splitlines()
            return api_key
        except:
            logging.info("Can't read api key. Create key.txt file and paste api_key there.")
            return None

    @staticmethod
    def logging_settings():
        return logging.basicConfig(level=logging.INFO,
                                   filemode='a',
                                   datefmt='%Y-%m-%d %H:%M:%S',
                                   format='%(levelname)s : %(asctime)s : %(message)s',
                                   filename='logs/BOT.log')
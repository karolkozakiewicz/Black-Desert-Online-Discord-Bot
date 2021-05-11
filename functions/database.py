from sqlalchemy import create_engine
import pandas as pd
from functions.bot_functions import Functions
import logging


class DatabaseSender():

    def __init__(self):
        Functions.logging_settings()
        self.ip = 'localhost'
        self.port = 5432
        self.username = 'username'
        self.password = 'password'
        self.database_name = 'dbname'
        self.engine = self.create_engine()

    def create_engine(self):
        try:
            conn = create_engine(
                f'postgresql://{self.username}:{self.password}@{self.ip}:{self.port}/{self.database_name}')
            if conn:
                return conn
            else:
                return False
        except Exception as e:
            logging.info(e)

    def add_to_database(self, data):
        df = pd.DataFrame.from_dict([data])
        df.to_sql(f"{df['server_id'][0]}",
                  con=self.engine,
                  index=False,
                  if_exists='append')

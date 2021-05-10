from sqlalchemy import create_engine
import pandas as pd

class DatabaseSender():

    def __init__(self, ip, port, username, password, database_name):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database_name
        self.engine = self.create_engine()

    def create_engine(self):
        return create_engine(f'postgresql://{self.username}:{self.password}@{self.ip}:{self.port}/{self.database_name}')

    def add_to_database(self, data):
        df = pd.DataFrame.from_dict([data])
        df.to_sql(f"{df['server_id'][0]}",
                  con=self.engine,
                  index=False,
                  if_exists='append')


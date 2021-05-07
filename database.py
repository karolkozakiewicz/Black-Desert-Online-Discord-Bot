import psycopg2


class PostGresConnection():

    def __init__(self, ip, port):
        if self.connection(ip, port):
            self.cursor = self.conn.cursor()

    def connection(self, ip, port):
        """
        :param ip: string
        :param port: int
        """
        try:
            conn = psycopg2.connect(
                host=ip,
                port=port,
                database="postgres",
                user="postgres",
                password="MIsiek08"
            )
            self.conn = conn
            print("Connected to database")
            return True
        except:
            print("Cannot get into database.")
            return False

    def create_new_table(self, data):
        self.conn.commit()
        print(data['guild_id'])
        query = f"""CREATE TABLE IF NOT EXISTS "{data['guild_id']}" (
                    "id" serial,
                    "guild_name" text,
                    "guild_id" numeric(50),
                    "channel_name" text,
                    "channel_id" numeric(50),
                    "author_nick" text,
                    "author_name" text,
                    "author_id" numeric(50),
                    "message" text,
                    PRIMARY KEY( id ));
                 """

        self.cursor.execute(query)
        self.conn.commit()


    def execute(self, query):
        """
        :param query: String SQL Query
        """
        try:
            self.cursor.execute(query)
        except psycopg2.Error as e:
            if str(type(e)).split("'")[1] == "psycopg2.errors.UndefinedTable":
                self.create_new_table(self.data)
                self.execute(query)
        except Exception as e:
            print(e)
        finally:
            self.conn.commit()
            try:
                response = self.cursor.fetchall()
                print(response)
            except:
                pass


    def insert_to_database(self, data):
        """
        :param data: dict containing:
                     guild_id -> bigint
                     guild_name -> string
                     channel_name -> string
                     channel_id -> bigint
                     author_nick -> string
                     author_name -> string
                     author_id -> bigint
                     message -> string
        """
        self.data = data
        guild_id = data['guild_id']
        guild_name = data['guild_name']
        channel_id = data['channel_id']
        channel_name = data['channel_name']
        author_nick = data['author_nick']
        author_name = data['author_name']
        author_id = data['author_id']
        message = data['message']
        query = f"""INSERT INTO public."{guild_id}"(
                    id, guild_name, guild_id, channel_name, channel_id, author_nick, author_name, author_id, message)
                    VALUES (DEFAULT, '{guild_name}', {guild_id},'{channel_name}','{channel_id}', '{author_nick}', 
                    '{author_name}', {author_id}, '{message}');
                 """
        self.execute(query)


    def get_data_from(self, database: str):
        """
        :param database: string table id
        """
        query = f"""SELECT * FROM "{database}" """
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        for i in response:
            print(i)

    def get_database_table_names(self):
        query = """SELECT table_name
                   FROM information_schema.tables
                   WHERE table_schema='public'
                   AND table_type='BASE TABLE';"""

        self.execute(query)


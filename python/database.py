import configparser
import mysql
import mysql.connector
from event import Event
from mysql.connector import errorcode


class Database(object):
    connection = {}
    event = Event('fire')
    rooms_table = []

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.host = config['MYSQL']['HOST']
        self.user = config['MYSQL']['USERNAME']
        self.password = config['MYSQL']['PASSWORD']
        self.database_name = 'domotipi'

    def open(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name)
            self.rooms_table = self.query_rooms()
            self.dispatch_event('connected')

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database does not exists')
            else:
                print(err)

    def remove_rooms(self):
        self.connection.connect()
        cursor = self.connection.cursor()
        cursor.execute("TRUNCATE TABLE rooms")
        self.connection.close()

    def query_rooms(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        print(rooms)
        self.connection.close()
        return rooms

    def dispatch_event(self, identifier):
        self.event(identifier)


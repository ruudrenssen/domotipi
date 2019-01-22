import configparser
import mysql
import mysql.connector
from event import Event
from mysql.connector import errorcode


class Database(object):
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
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name)
            self.rooms_table = self.query_rooms(connection)
            self.dispatch_event(self.rooms_table)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database does not exists')
            else:
                print(err)

    @staticmethod
    def query_rooms(connection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        connection.close()
        return rooms

    def dispatch_event(self, identifier):
        self.event(identifier)


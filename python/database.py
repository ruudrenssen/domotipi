import configparser
import mysql
import mysql.connector
from event import Event
from mysql.connector import errorcode


class Database(object):
    event = Event('fire')

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.host = config['MYSQL']['HOST']
        self.user = config['MYSQL']['USERNAME']
        self.password = config['MYSQL']['PASSWORD']
        self.database = 'domotipi'

    def open(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM groups_table")
            self.dispatch_event()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database does not exists')
            else:
                print(err)

    def dispatch_event(self):
        self.event('event content')

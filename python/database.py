import configparser
import mysql
import mysql.connector
from mysql.connector import errorcode


class Database(object):
    connection = {}
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

    def add_rooms(self, rooms):
        self.connection.connect()
        cursor = self.connection.cursor()
        for room in rooms:
            vendor_id = room.group_id
            name = room.name
            sql = """INSERT INTO rooms (name, vendor_id, hidden) VALUES ('%s', '%s', '%s')""" % (name, vendor_id, False)
            cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def remove_lights(self):
        self.connection.connect()
        cursor = self.connection.cursor()
        cursor.execute("TRUNCATE TABLE lights")
        self.connection.close()

    def add_lights(self, lights):
        self.connection.connect()
        cursor = self.connection.cursor()
        for light in lights:
            vendor_id = light.group_id
            name = light.name
            sql = """INSERT INTO rooms (name, vendor_id, hidden) VALUES ('%s', '%s', '%s')""" % (name, vendor_id, False)
            cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def query_rooms(self):
        self.connection.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        self.connection.close()
        return rooms


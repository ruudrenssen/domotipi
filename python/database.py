import configparser
import mysql
import mysql.connector
from mysql.connector import errorcode


class Database:
    def __init__(self, app):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.host = 'localhost'
        self.user = config['MYSQL']['USERNAME']
        self.password = config['MYSQL']['PASSWORD']
        self.database = 'domotipi'

        self.open()

    def open(self):
        try:
            cnx = mysql.connector.connect(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          database=self.database)
            connection = cnx
            session = cnx.cursor()
            session.execute("select * from groups_table")
            print(session.fetchall())
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('Database does not exists')
            else:
                print(err)

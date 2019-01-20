import configparser
from flask_mysqldb import MySQL


class Database:
    def __init__(self, app):
        config = configparser.ConfigParser()
        config.read('config.ini')
        username = config['MYSQL']['USERNAME']
        password = config['MYSQL']['PASSWORD']

        # Config MySQL
        app.config['MYSQL_HOST'] = '127.0.0.1'
        app.config['MYSQL_USER'] = username
        app.config['MYSQL_PASSWORD'] = password
        app.config['MYSQL_DB'] = 'domotipi'
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

        mysql = MySQL()

        print(mysql)

        # cursor = mysql.connection.cursor()

        # print(cursor.execute("GET * FROM " "group_table"))

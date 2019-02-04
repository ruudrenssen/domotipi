import configparser
import mysql
import mysql.connector
from mysql.connector import errorcode


class Database(object):
    connection = {}
    rooms_table = []

    def __init__(self):
        """ Load configuration """
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.host = config['MYSQL']['HOST']
        self.user = config['MYSQL']['USERNAME']
        self.password = config['MYSQL']['PASSWORD']
        self.database_name = 'domotipi'

    def open(self):
        """ Open MariaDB connection """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database_name)
            self.rooms_table = self.rooms()

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

    def rooms(self):
        """" Return all rooms """
        self.connection.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        self.connection.close()
        return rooms

    def remove_lights(self):
        self.connection.connect()
        cursor = self.connection.cursor()
        cursor.execute("TRUNCATE TABLE lights")
        self.connection.close()

    def add_lights(self, lights):
        self.connection.connect()
        cursor = self.connection.cursor()
        for light in lights:
            # execute sql based on type
            if light.type == "Extended color light":
                # process Philips Hue Extended Light
                self.add_extended_color_light(light, cursor)
            if light.type == "Color temperature light":
                # process Philips Hue Extended Light
                self.add_color_temperature_light(light, cursor)
            if light.type == "Dimmable light":
                # process Philips Hue Extended Light
                self.add_dimmable_color_light(light, cursor)
        self.connection.commit()
        self.connection.close()

    @staticmethod
    def add_dimmable_color_light(light, cursor):
        light_type = 'Dimmable light'
        name = light.name
        vendor_id = light.light_id
        reachable = light.reachable
        on_state = light.on
        brightness = light.brightness

        sql = """
        INSERT INTO lights 
        (name, vendor_id, on_state, reachable, type, brightness)
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" \
              % (name, vendor_id, on_state, reachable, light_type, brightness)
        cursor.execute(sql)

    @staticmethod
    def add_color_temperature_light(light, cursor):
        light_type = 'Color temperature light'
        name = light.name
        vendor_id = light.light_id
        reachable = light.reachable
        on_state = light.on
        colormode = light.colormode
        brightness = light.brightness
        colortemp = light.colortemp

        sql = """
        INSERT INTO lights 
        (name, vendor_id, on_state, reachable, type, brightness, colortemp, colormode)
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
              % (name, vendor_id, on_state, reachable, light_type, brightness, colortemp, colormode)
        cursor.execute(sql)

    @staticmethod
    def add_extended_color_light(light, cursor):
        light_type = 'Extended color light'
        name = light.name
        vendor_id = light.light_id
        reachable = light.reachable
        on_state = light.on
        brightness = light.brightness
        colormode = light.colormode
        colortemp = light.colortemp
        hue = light.hue
        saturation = light.saturation
        x_value = light.xy[0]
        y_value = light.xy[1]

        sql = """
        INSERT INTO lights 
        (name, vendor_id, on_state, reachable, type, brightness, colormode, colortemp, hue, saturation, x_value, y_value)
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
              % (name, vendor_id, on_state, reachable, light_type, brightness, colormode, colortemp, hue, saturation, x_value, y_value)
        cursor.execute(sql)

    def lights(self):
        """ Return all lights """
        self.connection.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM lights")
        lights = cursor.fetchall()
        self.connection.close()
        return lights


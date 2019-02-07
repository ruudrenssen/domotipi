import configparser
import mysql
import mysql.connector
from mysql.connector import errorcode


class Database(object):
    connection = {}

    def __init__(self):
        """ Load configuration """
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.host = config['MYSQL']['HOST']
        self.user = config['MYSQL']['USERNAME']
        self.password = config['MYSQL']['PASSWORD']
        self.database_name = 'domotipi'

        # Initialize database
        self.open_database()
        self.create_tables(self.connection.cursor())

    def open_database(self):
        try:
            self.set_connection()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                if err.errno == 1049:
                    """ No database named domotipi found. Create database domotpi """
                    connection = mysql.connector.connect(
                        host=self.host,
                        user=self.user,
                        password=self.password)
                    connection.connect()
                    cursor = connection.cursor()
                    sql = """CREATE DATABASE domotipi""" # todo: replace domotipi with config var
                    cursor.execute(sql)
                    connection.commit()
                    connection.close()

                    self.set_connection()
            else:
                print(err)

    def set_connection(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database_name)

    def config_database(self):
        self.connection.connect()
        cursor = self.connection.cursor()

        # Pick first room from DB if default_room does not exist and set is as default_room
        sql = """SELECT id FROM rooms"""
        cursor.execute(sql)
        default_room = cursor.fetchall()
        sql = """INSERT INTO `config` (property, value)
            SELECT * FROM (SELECT 'default_room', '%s') AS dummy_table
            WHERE NOT EXISTS (SELECT property FROM config WHERE property = `default_room`)""" % default_room[0][0]
        cursor.execute(sql)

        # Query config table for return
        sql = """ SELECT * FROM config """
        cursor.execute(sql)
        config = cursor.fetchall()
        self.connection.commit()
        self.connection.close()
        return config

    def get_rooms(self):
        """ Return all rooms """
        self.connection.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        self.connection.close()
        return rooms

    def add_rooms(self, rooms):
        self.connection.connect()
        cursor = self.connection.cursor()
        for room in rooms:
            vendor_id = room.group_id
            name = room.name
            brightness = room.brightness
            sql = """INSERT INTO rooms (name, vendor_id, hidden, brightness) VALUES ('%s', '%s', '%s', '%s')""" % (name, vendor_id, 0, brightness)
            cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def get_room(self, room_id):
        self.connection.connect()
        cursor = self.connection.cursor()
        sql = """SELECT * FROM rooms WHERE id='%s'""" % room_id
        cursor.execute(sql)
        room = cursor.fetchall()
        self.connection.commit()
        self.connection.close()
        return room

    def reset_rooms_table(self):
        self.connection.connect()
        cursor = self.connection.cursor()
        cursor.execute("TRUNCATE TABLE rooms")
        self.connection.close()

    def get_lights(self):
        # Return all lights
        self.connection.connect()
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM lights")
        lights = cursor.fetchall()
        self.connection.close()
        return lights

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

    def reset_lights_table(self):
        self.connection.connect()
        cursor = self.connection.cursor()
        cursor.execute("TRUNCATE TABLE lights")
        self.connection.close()

    @staticmethod
    def add_dimmable_color_light(light, cursor):
        """ Philips Hue Dimmable Light """
        light_type = 'Dimmable light'
        name = light.name
        vendor_id = light.light_id - 1
        reachable = int(light.reachable)
        on_state = int(light.on)
        brightness = light.brightness

        sql = """
            INSERT INTO lights (
            `type`, `name`, `vendor_id`, `reachable`, `on`, `brightness`) 
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s')""" \
              % (light_type, name, vendor_id, reachable, on_state, brightness)
        cursor.execute(sql)

    @staticmethod
    def add_color_temperature_light(light, cursor):
        """ Philips Hue Color Temperature Light """
        light_type = 'Color temperature light'
        name = light.name
        vendor_id = light.light_id - 1
        reachable = int(light.reachable)
        on_state = int(light.on)
        colormode = light.colormode
        brightness = light.brightness
        colortemp = light.colortemp

        sql = """INSERT INTO lights (
            `type`, `name`, `vendor_id`, `reachable`, `on`, `brightness`, `colormode`, `colortemp`) 
            VALUES (
            '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
              % (light_type, name, vendor_id, reachable, on_state, brightness, colormode, colortemp)
        cursor.execute(sql)

    @staticmethod
    def add_extended_color_light(light, cursor):
        """ Philips Hue Extended Color Light """
        light_type = 'Extended color light'
        name = light.name
        vendor_id = light.light_id - 1
        reachable = int(light.reachable)
        on_state = int(light.on)
        brightness = light.brightness
        colormode = light.colormode
        colortemp = light.colortemp
        hue = light.hue
        saturation = light.saturation
        x_value = light.xy[0]
        y_value = light.xy[1]

        sql = """
            INSERT INTO lights (
            `type`, `name`, `vendor_id`, `reachable`, `on`, `brightness`, 
            `colormode`, `colortemp`, `hue`, `saturation`, `x_value`, `y_value`) 
            VALUES (
            '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
              % (light_type, name, vendor_id, reachable, on_state, brightness,
                 colormode, colortemp, hue, saturation, x_value, y_value)
        cursor.execute(sql)

    def add_light_to_room(self, light_id, room_id):
        self.connection.connect()
        cursor = self.connection.cursor()
        sql = """ INSERT INTO rooms_lights (room_id, light_id) VALUES ('%s', '%s') """ % (room_id, light_id)
        cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def all_lights_from_room(self, room_id):
        self.connection.connect()
        cursor = self.connection.cursor()
        sql = """SELECT * FROM lights INNER JOIN rooms_lights ON lights.id=rooms_lights.light_id WHERE room_id='%s'
                """ % room_id
        cursor.execute(sql)
        lights = cursor.fetchall()
        self.connection.close()
        return lights

    def remove_all_lights_from_room(self, room_id):
        self.connection.connect()
        cursor = self.connection.cursor()
        sql = """DELETE FROM rooms_lights WHERE room_id='%s'""" % room_id
        cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    @staticmethod
    def create_tables(cursor):
        # Create config table if it doesn't already exist
        sql = """CREATE TABLE IF NOT EXISTS `domotipi`.`config` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `property` varchar(255) NOT NULL,
            `value` varchar(255) NOT NULL,
            PRIMARY KEY (`ID`))
            ENGINE = InnoDB;"""
        cursor.execute(sql)

        # Create scenes table if it doesn't already exist
        sql = """CREATE TABLE IF NOT EXISTS `domotipi`.`rooms` (
            `id` INT(3) NOT NULL AUTO_INCREMENT , 
            `name` VARCHAR(32) NOT NULL , 
            `vendor_id` INT NOT NULL ,  
            `hidden` BOOLEAN NOT NULL , 
            `brightness` TINYINT(3) UNSIGNED NOT NULL ,
            PRIMARY KEY (`id`)) 
            ENGINE = InnoDB;"""
        cursor.execute(sql)

        # Create lights table if it doesn't already exist
        sql = """CREATE TABLE IF NOT EXISTS `domotipi`.`lights` (
            `id` INT(3) NOT NULL AUTO_INCREMENT , 
            `type` VARCHAR(64) NOT NULL , 
            `name` VARCHAR(32) NOT NULL , 
            `vendor_id` INT NOT NULL , 
            `reachable` TINYINT(1) NOT NULL , 
            `on` TINYINT(1) NOT NULL , 
            `brightness` TINYINT(3) UNSIGNED , 
            `colormode` VARCHAR(64) , 
            `colortemp` SMALLINT , 
            `hue` SMALLINT(5) , 
            `saturation` TINYINT(3) UNSIGNED , 
            `x_value` DECIMAL(6) , 
            `y_value` DECIMAL(6) , 
            PRIMARY KEY (`id`))
            ENGINE = InnoDB;"""
        cursor.execute(sql)

        # Create rooms table if it doesn't already exist
        sql = """ CREATE TABLE IF NOT EXISTS `domotipi`.`rooms_lights` (
            `room_id` INT(3) NOT NULL  , 
            `light_id` INT NOT NULL ,
            PRIMARY KEY (`room_id`, `light_id`))
            ENGINE = InnoDB;"""
        cursor.execute(sql)

        # Create scenes table if it doesn't already exist
        sql = """CREATE TABLE IF NOT EXISTS `domotipi`.`scenes` (
            `id` INT(3) NOT NULL AUTO_INCREMENT ,
            `name` VARCHAR(32) NOT NULL ,
            `room_id` INT(3) NOT NULL , 
            `table_name` INT(3) NOT NULL ,
            PRIMARY KEY (`id`))
            ENGINE = InnoDB;"""
        cursor.execute(sql)

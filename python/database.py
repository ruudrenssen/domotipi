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

    def open(self):
        """ Open MariaDB connection """
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

    def rooms(self):
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
            sql = """INSERT INTO rooms (name, vendor_id, hidden, brightness) VALUES ('%s', '%s', '%s', '%s')""" % (name, vendor_id, False, brightness)
            cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def reset_rooms_table(self):
        self.connection.connect()
        cursor = self.connection.cursor()
        try:
            cursor.execute("TRUNCATE TABLE rooms")
        except mysql.connector.Error as err:
            # create new table for rooms
            sql = """ CREATE TABLE `domotipi`.`rooms` 
                    ( `id` INT(3) NOT NULL AUTO_INCREMENT ,
                    `name` VARCHAR(32) NOT NULL , 
                    `vendor_id` INT NOT NULL ,  
                    `hidden` BOOLEAN NOT NULL , 
                    `brightness` TINYINT(3) UNSIGNED NOT NULL ,
                    PRIMARY KEY (`id`)) 
                    ENGINE = InnoDB; """
            cursor.execute(sql)
        self.connection.close()

    def lights(self):
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
        try:
            cursor.execute("TRUNCATE TABLE lights")
        except mysql.connector.Error as err:
            # create new lights table
            sql = """CREATE TABLE `domotipi`.`lights` 
            ( `id` INT(3) NOT NULL AUTO_INCREMENT , 
            `type` VARCHAR(64) NOT NULL , 
            `name` VARCHAR(32) NOT NULL , 
            `vendor_id` INT NOT NULL , 
            `reachable` BOOLEAN NOT NULL , 
            `on` BOOLEAN NOT NULL , 
            `brightness` TINYINT(3) UNSIGNED , 
            `colormode` VARCHAR(64) NOT NULL , 
            `colortemp` SMALLINT NOT NULL , 
            `hue` SMALLINT(5) NOT NULL , 
            `saturation` TINYINT(3) UNSIGNED , 
            `x_value` DECIMAL(6) NOT NULL , 
            `y_value` DECIMAL(6) NOT NULL , 
            PRIMARY KEY (`id`)) 
            ENGINE = InnoDB; """
            cursor.execute(sql)
        self.connection.close()

    @staticmethod
    def add_dimmable_color_light(light, cursor):
        """ Philips Hue Dimmable Light """
        light_type = 'Dimmable light'
        name = light.name
        vendor_id = light.light_id
        reachable = light.reachable
        on_state = light.on
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
        vendor_id = light.light_id
        reachable = light.reachable
        on_state = light.on
        colormode = light.colormode
        brightness = light.brightness
        colortemp = light.colortemp

        sql = """
                    INSERT INTO lights (
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
        sql = """
        INSERT INTO rooms_lights
        (room_id, light_id)
        VALUES ('%s', '%s')
        """ % (room_id, light_id)
        cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def remove_all_lights_from_group(self, room_id):
        self.connection.connect()
        cursor = self.connection.cursor()
        sql = """
                DELETE FROM rooms_lights WHERE room_id='%s'
                """ % room_id
        try:
            cursor.execute(sql)
        except mysql.connector.Error as err:
            # create new table for rooms
            sql = """CREATE TABLE `domotipi`.`rooms_lights` 
                            (`room_id` INT NOT NULL , 
                            `light_id` INT NOT NULL ,
                            PRIMARY KEY (`room_id`, `light_id`)) 
                            ENGINE = InnoDB;"""
            cursor.execute(sql)
        self.connection.commit()
        self.connection.close()

    def set_connection(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database_name)

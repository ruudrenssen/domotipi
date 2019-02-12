import threading

class Rooms:
    rooms = []
    database = {}

    def __init__(self, database):
        self.database = database

    def sync_rooms(self, groups):
        # Sync vendor information with database
        self.database.reset_rooms_table()
        self.database.add_rooms(groups)
        for result in self.database.get_rooms():
            # Create new room object for each room, add lights based on vendor_id and add the room to the rooms object
            room = Room(self.database, result[0], result[1], result[2], result[3], result[4], result[5])
            room.sync_lights(groups[result[2]-1].lights)
            self.rooms.append(room)

    def get_rooms(self):
        return self.rooms


class Room:
    # Room properties
    room_id = ''
    room_name = ''
    vendor_id = 0
    hidden = False
    brightness = 125
    on = False
    database = {}

    # Available devices
    media_players = []
    lights = []

    def __init__(self, database, room_id=0, name='', vendor_id=0, hidden=False, brightness=125, on=False):
        self.room_id = room_id
        self.room_name = name
        self.vendor_id = vendor_id
        self.hidden = hidden
        self.on = on
        self.brightness = brightness
        self.database = database

    def sync_lights(self, lights):
        # Remove lights from rooms_lights table and lights object
        self.database.remove_all_lights_from_room(self.room_id)
        self.lights = []
        # Add lights to rooms_lights table and lights object
        brightness = 0
        for light in lights:
            self.database.add_light_to_room(light.light_id, self.room_id)
            brightness += light.brightness
            if light.on:
                self.on = True
            self.lights.append(light)

        self.brightness = int(brightness / len(lights))

    def get_lights(self):
        return self.lights

    def lights_on(self, bridge):
        self.on = True
        lights = []
        for light in self.lights:
            lights.append(light.light_id)
        command = {'on': True, 'bri': self.brightness}
        bridge.set_light(lights, command)

    def lights_fade(self, bridge, brightness, time):
        if brightness > 0:
            self.brightness = brightness
        lights = []
        for light in self.lights:
            lights.append(light.light_id)
        command = {'transitiontime': time, 'on': True, 'bri': brightness}
        bridge.set_light(lights, command)
        threading.Timer(time / 100, self.lights_off, [bridge]).start()

    def lights_fade_out(self, bridge, time):
        self.lights_fade(bridge, 0, time)
        threading.Timer(time/100, self.lights_off, [bridge]).start()

    def lights_off(self, bridge):
        self.on = False
        command = {'on': False}
        lights = []
        for light in self.lights:
            lights.append(light.light_id)
        bridge.set_light(lights, command)

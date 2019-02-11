class Rooms:
    rooms = []

    def sync_rooms(self, database, groups):
        # Sync vendor information with database
        database.reset_rooms_table()
        database.add_rooms(groups)
        for result in database.get_rooms():
            # Create new room object for each room, add lights based on vendor_id and add the room to the rooms object
            room = Room(result[0], result[1], result[2])
            room.sync_lights(database, groups[result[2]-1].lights)
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

    # Available devices
    media_players = []
    lights = []

    def __init__(self, room_id=0, name='', vendor_id=0, hidden=False, brightness=125):
        self.room_id = room_id
        self.room_name = name
        self.vendor_id = vendor_id
        self.hidden = hidden
        self.brightness = brightness

    def sync_lights(self, database, lights):
        # Remove lights from rooms_lights table and lights object
        database.remove_all_lights_from_room(self.room_id)
        self.lights = []
        # Add lights to rooms_lights table and lights object
        brightness = 0
        for light in lights:
            database.add_light_to_room(light.light_id, self.room_id)
            brightness += light.brightness
            if light.on:
                self.on = True
            self.lights.append(light)

        self.brightness = brightness / len(lights)
        print(self.brightness)

    def get_lights(self):
        return self.lights

    def dim_room(self):
        pass

    def set_scene(self, name):
        pass

    def lights_fade_out(self, time):
        pass

    def toggle_lights(seld):
        pass

class Rooms:
    rooms = []

    def sync_rooms(self, database, groups):
        """" Sync vendor information with database """
        database.reset_rooms_table()
        database.add_rooms(groups)
        for result in database.rooms():
            # Create new room object for each room, add lights based on vendor_id and add the room to the rooms object
            room = Room(result[0], result[1], result[2])
            room.sync_lights(database, groups[result[2]-1].lights)
            self.rooms.append(room)


class Room:
    """" Room properties and available devices """
    room_id = ''
    room_name = ''
    vendor_id = 0
    hidden = False

    media_players = []
    lights = []

    def __init__(self, room_id=0, name='', vendor_id=0, hidden=False):
        self.room_id = room_id
        self.room_name = name
        self.vendor_id = vendor_id
        self.hidden = hidden

    def sync_lights(self, database, lights):
        # Remove lights from rooms_lights table
        database.remove_all_lights_from_group(self.room_id)
        # Add lights to rooms_lights table
        for light in lights:
            database.add_light_to_room(light.light_id, self.room_id)

    @staticmethod
    def dim_room():
        pass

    @staticmethod
    def set_scene(name):
        pass

    @staticmethod
    def lights_fade_out(time):
        pass

    @staticmethod
    def lights_off():
        pass

class Rooms:
    rooms = []

    def sync_rooms(self, database, groups):
        database.event += self.clear_db_callback
        database.remove_rooms()

    @staticmethod
    def clear_db_callback(sender, identifier):
        if identifier == 'ROOMS_REMOVED':
            # rooms removed from database, create rooms based on hue
            pass

    def remove_room_by_id(self, identifier):
        pass

    def add_room(self, room_name):
        self.rooms.append(Room(self.rooms.count, room_name))


class Room:
    room_id = ''
    room_name = ''
    media_players = []
    lights = []
    light_groups = []

    def __init__(self, room_id, name):
        self.room_id = room_id
        self.room_name = name

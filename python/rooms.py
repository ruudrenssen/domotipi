class Rooms:
    rooms = []

    def sync_rooms(self, database, groups):
        print(database)
        print(groups[1].name)
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

    def __init__(self, id, name):
        self.room_id = id
        self.room_name = name
        print(id)

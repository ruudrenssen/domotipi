class Rooms:
    rooms = []

    def sync_rooms(self, database, groups):
        database.remove_rooms()
        database.add_rooms(groups)
        self.rooms = database.query_rooms()
        print(self.rooms)


class Room:
    room_id = ''
    room_name = ''
    media_players = []
    lights = []
    light_groups = []

    def __init__(self, room_id, name):
        self.room_id = room_id
        self.room_name = name

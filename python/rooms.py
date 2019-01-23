class Rooms:
    rooms = []

    def sync_rooms(self, database, groups):
        """" Sync vendor information with database """
        database.remove_rooms()
        database.add_rooms(groups)
        for result in database.rooms():
            room = Room(result[0], result[2], result[2])
            print(result)
            self.rooms.append(room)
        print(self.rooms)


class Room:
    """" Room properties and available devices """
    room_id = ''
    room_name = ''
    vendor_id = 0
    hidden = False

    media_players = []
    lights = []

    def __init__(self, room_id=0, name='', vendor_id=0, hidden = False):
        self.room_id = room_id
        self.room_name = name
        self.vendor_id = vendor_id
        self.hidden
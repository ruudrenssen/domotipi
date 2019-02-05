class Lights:
    lights = []

    def sync_lights(self, database, lights):
        """ Sync vendor information with database """
        database.reset_lights_table()
        database.add_lights(lights)
        # for result in database.lights():
        #     light = Light(result[0], result[2], result[2])
        #     self.rooms.append(light)


class Light:
    light_if = ''
    light_name = ''
    vendor_id = ''

    def __init__(self, light_id=0, name='', vendor_id=0):
        self.light_id = light_id
        self.light_name = name
        self.vendor_id = vendor_id

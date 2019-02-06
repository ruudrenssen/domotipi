class Lights:
    lights = []

    def sync_lights(self, database, lights):
        """ Sync vendor information with database """
        database.reset_lights_table()
        database.add_lights(lights)
        for result in database.lights():
            # create new light object based on type
            print(result)


class Light:
    light_id = ''
    light_name = ''
    vendor_id = ''
    reachable = False
    light_type = ''

    def __init__(self, light_type, light_id=0, name='', vendor_id=0, reachable = False):
        self.light_type = light_type
        self.light_id = light_id
        self.light_name = name
        self.vendor_id = vendor_id
        self.reachable = reachable

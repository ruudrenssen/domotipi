class Lights:
    lights = []

    def sync_lights(self, database, lights):
        """ Sync vendor information with database """
        database.reset_lights_table()
        database.add_lights(lights)
        for result in database.lights():
            # create new Light instance and pass the phue light object as parameter
            light = Light(lights[result[3]], result)
            self.lights.append(light)


class Light:
    def __init__(self, phue_light, db_row):
        self.light_id = db_row[0]
        self.light_type = db_row[1]
        self.light_name = db_row[2]
        self.vendor_id = db_row[3]
        self.reachable = db_row[4]
        self.on_state = db_row[5]
        self.brightness = db_row[6]
        self.colormode = db_row[7]
        self.colortemp = db_row[8]
        self.hue = db_row[9]
        self.saturation = db_row[10]
        self.x_value = db_row[11]
        self.y_value = db_row[12]
        self.phue = phue_light


    def toggle_on(light):
        light.on_state = not light.on_state
        light.phue.on = light.on_state
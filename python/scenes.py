import threading
import random


class Scenes:
    scenes = []
    database = {}

    def __init__(self, database):
        self.database = database

    def sync_scenes(self, bridge):
        scenes = bridge.get_scene().items()
        self.database.reset_scenes_table()
        self.database.add_scenes(scenes)

        for result in self.database.get_scenes():
            # Create new scene object for each room, add lights based on vendor_id and add the scene to the rooms object
            scene = Scene(result[0], result[1], result[2], result[3], result[4])
            self.scenes.append(scene)

    def get_scenes_for_room(self, room_id):
        self.database.connection.connect()
        cursor = self.database.connection.cursor()
        sql = """SELECT * FROM scenes WHERE room_id = %s""" % room_id
        cursor.execute(sql)
        scenes = cursor.fetchall()
        self.database.connection.close()
        return scenes

    @staticmethod
    def activate_scene(bridge, scene_proporties):
        scene_id = scene_proporties['scene_id']
        room_id = scene_proporties['room_id']
        print(bridge.activate_scene(room_id, scene_id))


class Scene:
    name = ''
    scene_type = ''
    lights = ''
    room_id = ''
    vendor_id = ''

    def __init__(self, name, scene_type, lights, room_id, vendor_id):
        self.name = name
        self.scene_type = scene_type
        self.room_id = room_id
        self.lights = lights.split()
        self.vendor_id = vendor_id

    def activate_scene(self):
        pass


class LivingScene(Scene):
    def __init__(self, room_id, lights):
        super().__init__(room_id, lights)
        self.name = 'Living scene'

        # filter extended color lights and store in light object
        lights = []
        for light in self.lights:
            if light.type == 'Extended color light':
                lights.append(light)
        self.lights = lights

    def refresh_scene(self, bridge, colors):
        i = 0
        for light in self.lights:
            # start color looping through extended color lights
            command = {'transitiontime': 45, 'on': True, 'bri': 254, 'hue': colors[i][0], 'sat': 254}
            bridge.set_light(light.light_id, command)
            i += 1
        colors.append(colors.pop(0))
        threading.Timer(5, self.refresh_scene, [bridge, colors]).start()

    def activate_scene(self, bridge):
        light_count = self.lights.__len__()
        self.refresh_scene(bridge, self.generate_random_color(light_count))

    @staticmethod
    def generate_random_color(light_count):
        colors = []
        i = 0
        light_count = light_count + 1
        step_size = int(65534/light_count)
        while i < light_count:
            hue = step_size * (i + 1)
            saturation = random.randint(200, 254)
            color = [hue, saturation]
            colors.append(color)
            i += 1

        return colors


class Dimmed(Scene):
    def __init__(self, room_id, lights):
        super().__init__(room_id, lights)
        self.name = 'Dimmed'

    def activate_scene(self, bridge):
        for light in self.lights:
            command = {'transitiontime': 5, 'on': True, 'bri': 50}
            bridge.set_light(light.light_id, command)


class DaylightScene(Scene):
    def __init__(self, room_id, lights):
        super().__init__(room_id, lights)
        self.name = 'Daylight'

    def activate_scene(self, bridge):
        for light in self.lights:
            command = {'transitiontime': 5, 'on': True, 'bri': 254, 'ct': 366}
            bridge.set_light(light.light_id, command)


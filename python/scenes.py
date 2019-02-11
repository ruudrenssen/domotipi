import threading
import random

class Scenes:
    scenes = []

    def initialize_scenes(self, rooms):
        for room in rooms:
            scenes = []
            room_id = room.room_id
            lights = []
            for light in room.get_lights():
                lights.append(light)

            scene = DaylightScene(room_id, lights)
            scenes.append(scene)

            scene = Dimmed(room_id, lights)
            scenes.append(scene)

            scene = LivingScene(room_id, lights)
            scenes.append(scene)

            self.scenes.insert(room_id, scenes)

    def get_scenes_for_room(self, room_id):
        return self.scenes[room_id-1]


class Scene:
    scene_id = ''
    name = ''
    room_id = ''
    lights = []

    def __init__(self, room_id, lights):
        self.room_id = room_id
        self.lights = lights

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


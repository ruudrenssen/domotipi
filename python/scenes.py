import threading
import random

class Scenes:
    scenes = []

    def initialize_scenes(self, rooms):
        for room in rooms:
            rooms = []
            room_id = room.room_id
            lights = []
            for light in room.get_lights():
                lights.append(light)

            scene = DaylightScene(room_id, lights)
            rooms.append(scene)

            scene = LivingScene(room_id, lights)
            rooms.append(scene)

            scene = LightsOffScene(room_id, lights)
            rooms.append(scene)

            self.scenes.append(rooms)

    def get_scenes(self):
        return self.scenes


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
            print(light.type)
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
        step_size = int(65534/light_count)
        while i < light_count:
            hue = step_size * (i + 1)
            saturation = random.randint(200, 254)
            color = [hue, saturation]
            colors.append(color)
            i += 1

        return colors


class LightsOffScene(Scene):
    def activate_scene(self, bridge):
        for light in self.lights:
            command = {'transitiontime': 5, 'on': True, 'bri': 0}
            bridge.set_light(light.light_id, command)


class DaylightScene(Scene):
    def activate_scene(self, bridge):
        for light in self.lights:
            command = {'transitiontime': 5, 'on': True, 'bri': 254, 'ct': 366}
            bridge.set_light(light.light_id, command)


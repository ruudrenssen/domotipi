class Scenes:
    scenes = []

    def initialize_scenes(self, rooms):
        for room in rooms:
            for light in room.get_lights():
                print(light)

class Scene:
    scene_id = ''
    name = ''
    room_id = ''
    lights = []

    @staticmethod
    def activate_scene():
        pass

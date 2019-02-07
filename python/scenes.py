class Scenes:
    scenes = []

    def sync_scenes(self, database):
        database.reset_scenes_table()

class Scene:
    name = ''
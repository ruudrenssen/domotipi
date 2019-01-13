import configparser
from phue import Bridge

class Hue():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['HUE']['IP_ADDRESS']

        self.bridge = Bridge(ip)
        self.light_groups = self.bridge.groups
        self.lights = self.bridge.lights

        # for group in self.lightgroups:
        #     print(group)
        #
        # for light in self.lights:
        #     print (light)

    def transitionToBright(self, light, seconds):
        self.bridge.set_light(light.name, 'bri', 125, transitiontime = (seconds * 10))

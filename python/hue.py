import configparser
from phue import Bridge

class Hue():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['HUE']['IP_ADDRESS']

        self.bridge = Bridge(ip)
        self.bridge.connect()
        lightgroups = self.bridge.groups
        lights = self.bridge.lights

        for group in lightgroups:
            print(group)

        for light in lights:
            print (light)

    def setToBright(self, light):
        self.bridge.set_light(light.name, 'bri', 255, transitiontime = 1)

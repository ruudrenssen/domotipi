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

    def transitionToBright(self, light, seconds):
        self.bridge.set_light(light.name, 'bri', 125, transitiontime = (seconds * 10))


class Light():
    def __init__(self):
        self._light_id
        self._name
        self._on
        self._reachable
        self._type

class DimmableLight(Light):
    def __init__(self):
        self._brightness
        self._alert

class TemperatureLight(DimmableLight):
    def __init__(self):
        self._colortemparture
        self._colormode

class ExtendedLight(TemperatureLight):
    def __init__(self):
        self._xy
        self._hue
        self._saturation
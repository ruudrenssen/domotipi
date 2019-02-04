import configparser
import distutils.util
from phue import Bridge


class Hue:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['HUE']['IP_ADDRESS']

        self.bridge = Bridge(ip)

        if self.connect_to_hue(self.bridge):
            self.rooms = self.bridge.groups
            self.lights = self.bridge.lights
            print('lights and rooms loaded')

    @staticmethod
    def connect_to_hue(bridge):
        try:
            bridge.connect()
            return True
        except Exception as exception:
            print(exception)
            return False

    def transition_to_bright(self, light, seconds):
        self.bridge.set_light(light.name, 'bri', 254, transitiontime=(seconds * 10))

    def transform_light(self, form):
        # copy form in order to mutate
        form = form.copy()

        # get light_id and strip it from the form object
        light_id = int(form.pop('light_id').strip('light_'))

        """" Set light properties """
        if 'on' in form:
            form['on'] = bool(distutils.util.strtobool(form['on']))
        elif 'colortemp' in form:
            form['colortemp'] = int(form['colortemp'])
        elif 'brightness' in form:
            form['brightness'] = int(form['brightness'])
        elif 'colormode' in form:
            # Color mode changed. Set var specific to that mode to change light mode on hue bridge
            if form['colormode'] == 'xy':
                setattr(self.lights[light_id - 1], 'xy', getattr(self.lights[light_id - 1], 'xy'))
                return
            elif form['colormode'] == 'hs':
                setattr(self.lights[light_id - 1], 'hue', getattr(self.lights[light_id - 1], 'hue'))
                return
            elif form['colormode'] == 'ct':
                setattr(self.lights[light_id - 1], 'colortemp', getattr(self.lights[light_id - 1], 'colortemp'))
                return

        """" All other properties have compatiable values with the form, execute in loop """
        for light_property in form:
            setattr(self.lights[light_id-1], light_property, form[light_property])

import configparser
import distutils.util
from phue import Bridge


class Hue():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['HUE']['IP_ADDRESS']

        self.bridge = Bridge(ip)
        self.light_groups = self.bridge.groups
        self.lights = self.bridge.lights

    def transition_to_bright(self, light, seconds):
        self.bridge.set_light(light.name, 'bri', 125, transitiontime = (seconds * 10))

    def process_form(self, form):
        form = form.copy()
        light_id = int(form.pop('light_id').strip('light_'))

        if 'on' in form:
            print(form['on'])
            form['on'] = bool(distutils.util.strtobool(form['on']))
            print(form['on'])

        if 'colortemp' in form:
            form['colortemp'] = int(form['colortemp'])

        for property in form:
            # print(property)
            # print(form[property])
            setattr(self.lights[light_id-1], property, form[property])

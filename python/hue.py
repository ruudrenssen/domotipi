import configparser
import distutils.util
from phue import Bridge


class Hue:
    rooms = {}
    lights = {}
    scenes = {}

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['HUE']['IP_ADDRESS']
        user = config['HUE']['USER']
        self.bridge = Bridge(ip, user)

        try:
            self.bridge.connect()
        except ConnectionError as err:
            print(err)

        self.rooms = self.bridge.groups
        self.lights = self.bridge.lights
        self.scenes = self.bridge.get_scene()

        # print(self.bridge.get_sensor_objects())
        for sensor in self.bridge.get_sensor_objects():
            print(sensor.__dict__)
            # print('sensor_id: ' + str(sensor.sensor_id))
            # print('name: ' + str(sensor.name))
            print('config: ' + str(sensor.config))
            # print('type: ' + str(sensor.type))
            print('state: ' + str(sensor.state))
            # print('modelid: ' + str(sensor.modelid))
            # print('recycle: ' + str(sensor.recycle))
            pass

        # print(self.scenes.__dir__())
        # for key in self.scenes.keys():
        #     print(key)


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

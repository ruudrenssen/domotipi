from flask import Flask, render_template, request, redirect
from wtforms import Form, FormField, FieldList, StringField, BooleanField, IntegerField, HiddenField
from kodi import KodiRemote
from hue import Hue

kodi = KodiRemote()
hue = Hue()
app = Flask(__name__)


class KodiForm(Form):
    kodi_action = StringField()


class LightForm(Form):
    light_id = HiddenField()
    name = StringField()
    on = BooleanField()
    brightness = IntegerField()
    saturation = IntegerField()
    hue = IntegerField()


class HueForm(Form):
    hue_action = FieldList(FormField(LightForm), min_entries=0)


@app.route('/')
def index():
    light_info_fields = []
    for light in hue.lights:
        light_field = {}

        type_value = getattr(light, 'type')
        light_field['type'] = type_value

        if type_value == 'Extended color light':
            properties = ['light_id',
                          'name',
                          'on',
                          'brightness',
                          'colormode',
                          'hue',
                          'xy',
                          'colortemp',
                          'effect',
                          'alert',
                          'reachable']
            light_info_fields.append(create_fields(light, light_field, properties))

        if type_value == 'Color temperature light':
            properties = ['light_id',
                          'name',
                          'on',
                          'brightness',
                          'colormode',
                          'colortemp',
                          'alert',
                          'reachable']
            light_info_fields.append(create_fields(light, light_field, properties))

        if type_value == 'Dimmable light':
            properties = ['light_id',
                          'name',
                          'on',
                          'brightness',
                          'alert',
                          'reachable']
            light_info_fields.append(create_fields(light, light_field, properties))

    form = HueForm(hue_action=light_info_fields)
    return render_template('room.html', form=form.hue_action)


def create_fields(light_obj, field_obj, properties):
    for light_property in properties:
        field_obj[light_property] = getattr(light_obj, light_property)
    print(field_obj)
    return field_obj


@app.route('/hue', methods=['POST', 'GET'])
def hue_action():
    return redirect("/", code=302)


@app.route('/kodi', methods=['POST', 'GET'])
def kodi_action():
    form = KodiForm(request.form)
    getattr(kodi, form.kodi_action.data)()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
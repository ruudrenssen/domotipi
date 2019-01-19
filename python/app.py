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
    light_id = StringField()
    name = StringField()
    type = StringField()
    on = BooleanField()
    colortemp = IntegerField()
    saturation = IntegerField()
    hue = IntegerField()
    xy = StringField()
    colormode = StringField()
    effect = StringField()
    alert = StringField()
    reachable = StringField()
    brightness = IntegerField()
    colormode = StringField()
#
# class DimmableLightForm(Form):
#
# class ExtendedLightForm(Form):


class HueForm(Form):
    hue_light_info = FieldList(FormField(LightForm), min_entries=0)


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
                          'type',
                          'on',
                          'brightness',
                          'saturation',
                          'colormode',
                          'hue',
                          'xy',
                          'colortemp',
                          'effect',
                          'alert']
            light_info_fields.append(create_fields(light, light_field, properties))

        if type_value == 'Color temperature light':
            properties = ['light_id',
                          'name',
                          'type',
                          'on',
                          'brightness',
                          'colortemp',
                          'colormode',
                          'alert']
            light_info_fields.append(create_fields(light, light_field, properties))

        if type_value == 'Dimmable light':
            properties = ['light_id',
                          'name',
                          'type',
                          'on',
                          'brightness',
                          'alert']
            light_info_fields.append(create_fields(light, light_field, properties))

    form = HueForm(hue_light_info=light_info_fields)
    return render_template('all.html', form=form.hue_light_info)


def create_fields(light_obj, field_obj, properties):
    for light_property in properties:
        field_obj[light_property] = getattr(light_obj, light_property)
    return field_obj


@app.route('/hue', methods=['POST', 'GET'])
def hue_light_info():
    form = request.form.copy()
    print(form)
    light_id = int(form.pop('light_id').strip('light_'))
    form['on'] = bool(form['on'])
    if 'colortemp' in form:
        form['colortemp'] = int(form['colortemp'])
    for field in form:
        print(field + ': ' + str(getattr(hue.lights[light_id-1], field)))
        print(form[field])
        setattr(hue.lights[light_id-1], str(field), form[field])
    return redirect("/", code=302)


@app.route('/kodi', methods=['POST', 'GET'])
def kodi_action():
    form = KodiForm(request.form)
    getattr(kodi, form.kodi_action.data)()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)

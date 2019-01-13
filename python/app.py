from flask import Flask, render_template, request, redirect
from wtforms import Form, FormField, FieldList, StringField
from kodi import KodiRemote
from hue import Hue

kodi = KodiRemote()
hue = Hue()
app = Flask(__name__)


class KodiForm(Form):
    kodi_action = StringField()


class LightForm(Form):
    name = StringField()


class HueForm(Form):
    hue_action = FieldList(FormField(LightForm), min_entries=0)


@app.route('/')
def index(hue_data=hue):
    light_fields = []
    for light in hue.lights:
        light_field = {'name': light.name}
        light_fields.append(light_field)
    form = HueForm(hue_action=light_fields)
    print(form.hue_action.data)
    return render_template('room.html', form=form.hue_action)


@app.route('/hue', methods=['POST', 'GET'])
def hue_action():
    form = HueForm(request.form)
    print(form.hue_action.data)
    return redirect("/", code=302)


@app.route('/kodi', methods=['POST', 'GET'])
def kodi_action():
    form = KodiForm(request.form)
    getattr(kodi, form.kodi_action.data)()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
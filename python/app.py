from flask import Flask, render_template, request, redirect
from wtforms import Form, FormField, FieldList, StringField
from kodi import KodiRemote
from lights import Hue


kodi = KodiRemote()
lights = Hue()
app = Flask(__name__)


class KodiForm(Form):
    kodi_action = StringField('kodiaction')


class HueForm(Form):
    lights = FieldList(FormField(StringField), min_entries = 0)


@app.route('/')
def index(hue = lights):
    return render_template('room.html', lights = hue.lights)


@app.route('/hue', methods=['POST', 'GET'])
def hue(hue = lights):
    form = HueForm(request.form)
    for light in hue.lights:
        print(getattr(form, 'light' + str(light.light_id)))
    return redirect("/", code=302)


@app.route('/kodi', methods=['POST', 'GET'])
def kodi_action():
    form = KodiForm(request.form)
    getattr(kodi, form.kodi_action.data)()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
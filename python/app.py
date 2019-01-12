from flask import Flask, render_template, request, redirect
from wtforms import Form, StringField
from kodi import KodiRemote
from hue import Hue

kodi = KodiRemote()
hue = Hue()
app = Flask(__name__)


class KodiForm(Form):
    kodiaction = StringField('kodiaction')


class HueForm(Form):
    lightid = StringField('light')
    action = StringField('action')


@app.route('/')
def index(hue = hue):
    return render_template('room.html', lights = hue.lights)

@app.route('/hue', methods=['POST', 'GET'])
def hue(hue = hue):
    form = HueForm(request.form)
    return redirect("/", code=302)


@app.route('/kodi', methods=['POST', 'GET'])
def kodiaction():
    form = KodiForm(request.form)
    getattr(kodi, form.kodiaction.data)()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
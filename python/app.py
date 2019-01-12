from flask import Flask, render_template, request, redirect
from wtforms import Form, StringField
from kodi import KodiRemote
from hue import Hue

kodi = KodiRemote()
hue = Hue()

app = Flask(__name__)


class KodiForm(Form):
    action = StringField('action')


class HueForm(Form):
    lightid = StringField('light')
    action = StringField('action')


@app.route('/')
def index():
    return render_template('room.html')


@app.route('/kodi', methods=['POST', 'GET'])
def action():
    form = KodiForm(request.form)
    getattr(kodi, form.action.data)()
    return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
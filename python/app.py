from flask import Flask, render_template, request, redirect
from kodi import KodiRemote
from hue import Hue
from database import Database

app = Flask(__name__)
db = Database()
kodi = KodiRemote()
hue = Hue()


def callback(sender, earg):
    print(sender)
    print(earg)


@app.route('/')
def index():
    return render_template('all.jinja', lights=hue.lights)


@app.route('/hue', methods=['POST', 'GET'])
def hue_light_info():
    form = request.form
    hue.process_form(form)
    return redirect("/", code=302)


@app.route('/kodi', methods=['POST', 'GET'])
def kodi_action():
    form = request.form
    getattr(kodi, form['kodi_action'])()
    return redirect("/", code=302)


if __name__ == '__main__':
    db.event += callback
    db.open()
    app.run(debug=True)

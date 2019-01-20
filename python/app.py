from flask import Flask, render_template, request, redirect
from kodi import KodiRemote
from hue import Hue
from database import Database

app = Flask(__name__)
db = Database(app)
kodi = KodiRemote()
hue = Hue()


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
    app.run(debug=True)

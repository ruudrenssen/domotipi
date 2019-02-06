from flask import Flask, render_template, request, redirect
from kodi import KodiRemote
from hue import Hue
from database import Database
from rooms import Rooms
from lights import Lights

app = Flask(__name__)
hue = Hue()
kodi = KodiRemote()
db = Database()
rooms = Rooms()
lights = Lights()


""" Prepare the database """
config = db.config()
lights.sync_lights(db, hue.lights)
rooms.sync_rooms(db, hue.rooms)


@app.route('/')
def index():
    """ Default route """
    return redirect("/room/woonkamer", code=302)


@app.route('/room/<room_name>')
def room(room_name):
    return render_template('room.jinja', name=room_name)


@app.route('/all-lights')
def all_lights():
    """ All lights setup """
    return render_template('lights.jinja', lights=hue.lights)


@app.route('/hue', methods=['POST', 'GET'])
def hue_light_info():
    """ Handle Phillips Hue commands """
    form = request.form
    hue.transform_light(form)
    return redirect("/", code=302)


@app.route('/kodi', methods=['POST', 'GET'])
def kodi_action():
    """ Handle Kodi media player commands """
    form = request.form
    getattr(kodi, form['kodi_action'])()
    return redirect("/", code=302)


""" Run the app """
if __name__ == '__main__':
    app.run(debug=True)

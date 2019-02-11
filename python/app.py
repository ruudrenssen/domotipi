from flask import Flask, render_template, request, redirect
from kodi import KodiRemote
from hue import Hue
from database import Database
from rooms import Rooms
from lights import Lights
from scenes import Scenes

app = Flask(__name__)
hue = Hue()
kodi = KodiRemote()
db = Database()
rooms = Rooms()
lights = Lights()
scenes = Scenes()

# Prepare database: populate tables
lights.sync_lights(db, hue.lights)
rooms.sync_rooms(db, hue.rooms)

# setup scenes
scenes.initialize_scenes(rooms.get_rooms())

# scenes.get_scenes()[0][2].activate_scene(hue.bridge)
# scenes.get_scenes()[1][1].activate_scene(hue.bridge)


@app.route('/')
def index():
    """ Default route """
    config = db.config_database()
    return redirect("/room/" + config[0][2], code=302)


@app.route('/room/<room_id>')
def room(room_id):
    """ Route for room """
    kodi.update()
    room_scenes = scenes.get_scenes_for_room(int(room_id))
    return render_template('room.jinja',
                           current='media',
                           room=db.get_room(room_id),
                           lights=db.all_lights_from_room(room_id),
                           media=kodi.properties,
                           scenes=room_scenes)


@app.route('/room/<room_id>/lights')
def lights(room_id):
    """ Route for room """
    room_scenes = scenes.get_scenes_for_room(int(room_id))
    return render_template('lights.jinja',
                           current='lights',
                           room=db.get_room(room_id),
                           lights=db.all_lights_from_room(room_id),
                           scenes=room_scenes)


@app.route('/room/<room_id>/save-as-scene.jinja')
def save_scene(room_id):
    """ Route for room """
    return render_template('save-scene.jinja.jinja',
                           current='save-scene',
                           room=db.get_room(room_id),
                           lights=db.all_lights_from_room(room_id))


@app.route('/all-lights')
def all_lights():
    """ All lights setup """
    return render_template('lights.jinja',
                           lights=hue.lights)


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
    url = request.referrer
    getattr(kodi, form['kodi_action'])()
    return redirect(url, code=302)


""" Run the app """
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

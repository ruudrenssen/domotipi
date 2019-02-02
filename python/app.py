from flask import Flask, render_template, request, redirect
from kodi import KodiRemote
from hue import Hue
from database import Database
from rooms import Rooms

app = Flask(__name__)
kodi = KodiRemote()
hue = Hue()
db = Database()
rooms = Rooms()


@app.route('/')
def index():
    """" Default route """
    return render_template('all.jinja', lights=hue.lights)


@app.route('/hue', methods=['POST', 'GET'])
def hue_light_info():
    """" Handle Phillips Hue commands """
    form = request.form
    hue.process_form(form)
    return redirect("/", code=302)


@app.route('/kodi', methods=['POST', 'GET'])
def kodi_action():
    """" Handle Kodi media player commands """
    form = request.form
    getattr(kodi, form['kodi_action'])()
    return redirect("/", code=302)


"""" Prepare the database """
db.open()
# rooms.sync_rooms(db, hue.rooms)


"""" Run the app """
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
from kodi import KodiRemote

kodi = KodiRemote()

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/kodi/playpause')
def playpause():
    kodi.playpause()
    return render_template('home.html')

@app.route('/kodi/left')
def left():
    kodi.left()
    return render_template('home.html')

@app.route('/kodi/right')
def right():
    kodi.right()
    return render_template('home.html')

@app.route('/kodi/up')
def up():
    kodi.up()
    return render_template('home.html')

@app.route('/kodi/down')
def down():
    kodi.down()
    return render_template('home.html')

@app.route('/kodi/getmovies')
def getmovies():
    kodi.getmovies()
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
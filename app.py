from flask import Flask, render_template, request, redirect
from kodi import KodiRemote
from wtforms import Form, StringField

kodi = KodiRemote()

app = Flask(__name__)


class ActionForm(Form):
    action = StringField('action')


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/action', methods=['POST', 'GET'])
def action():
    form = ActionForm(request.form)
    eval(form.action.data)()
    print(form.action.data)
    return redirect("/", code=302)


def toggle_play():
    kodi.playpause()
    return render_template('home.html')


def left():
    kodi.left()
    return render_template('home.html')


def right():
    kodi.right()
    return render_template('home.html')


def up():
    kodi.up()
    return render_template('home.html')


def down():
    kodi.down()
    return render_template('home.html')


def getmovies():
    kodi.getmovies()
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
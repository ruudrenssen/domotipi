import configparser
from kodijson import Kodi, PLAYER_VIDEO


class KodiRemote():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['KODI']['IP_ADDRESS']
        self.kodi = Kodi('http://' + ip + '/jsonrpc')
        self.movieList = self.kodi.VideoLibrary.GetMovies()

    def get_movies(self):
        print(self.movieList)

    def left(self):
        self.kodi.Input.Left()

    def right(self):
        self. kodi.Input.Right()

    def up(self):
        self.kodi.Input.Up()

    def down(self):
        self.kodi.Input.Down()

    def back(self):
        self.kodi.Input.Back()

    def info(self):
        self.kodi.Input.Info()

    def playpause(self):
        self.kodi.Player.PlayPause([PLAYER_VIDEO])

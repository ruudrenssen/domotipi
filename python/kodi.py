import configparser
from kodijson import Kodi, PLAYER_VIDEO


class KodiRemote():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['KODI']['IP_ADDRESS']
        self.kodi = self.check_connection(ip)
        if self.kodi:
            print('connected to kodi')
        else:
            print('could not connect to kodi')

    def check_connection(self, ip):
        self.kodi = Kodi('http://' + ip + '/jsonrpc')
        try:
            self.kodi.JSONRPC.Ping()
            return self.kodi
        except:
            return False

    def get_movies(self, kodi):
        self.kodi.VideoLibrary.GetMovies()

    def left(self, kodi):
        self.kodi.Input.Left()

    def right(self, kodi):
        self.kodi.Input.Right()

    def up(self, kodi):
        self.kodi.Input.Up()

    def down(self, kodi):
        self.kodi.Input.Down()

    def back(self, kodi):
        self.kodi.Input.Back()

    def info(self, kodi):
        self.kodi.Input.Info()

    def select(self, kodi):
        self.kodi.Input.Select()

    def volume_up(self, kodi):
        pass

    def volume_down(self, kodi):
        pass

    def playpause(self, kodi):
        self.kodi.Player.PlayPause([PLAYER_VIDEO])

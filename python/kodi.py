import configparser
from kodijson import Kodi, PLAYER_VIDEO


class KodiRemote():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['KODI']['IP_ADDRESS']
        kodi = self.check_connection(ip)
        if kodi:
            print('connected to kodi')
        else:
            print('could not connect to kodi')

    @staticmethod
    def check_connection(ip):
        kodi = Kodi('http://' + ip + '/jsonrpc')
        try:
            kodi.JSONRPC.Ping()
            return kodi
        except:
            return False

    @staticmethod
    def get_movies(kodi):
        kodi.VideoLibrary.GetMovies()

    @staticmethod
    def left(kodi):
        kodi.Input.Left()

    @staticmethod
    def right(kodi):
         kodi.Input.Right()

    @staticmethod
    def up(kodi):
        kodi.Input.Up()

    @staticmethod
    def down(kodi):
        kodi.Input.Down()

    @staticmethod
    def back(kodi):
        kodi.Input.Back()

    @staticmethod
    def info(kodi):
        kodi.Input.Info()

    @staticmethod
    def playpause(kodi):
        kodi.Player.PlayPause([PLAYER_VIDEO])

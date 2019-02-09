import configparser
from kodijson import Kodi, PLAYER_VIDEO


class KodiRemote():
    properties = {
        'current_item': ''
    }

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        ip = config['KODI']['IP_ADDRESS']
        self.kodi = self.check_connection(ip)
        if self.kodi:
            print('connected to kodi')
        else:
            print('could not connect to kodi')

        self.update()

    def update(self):
        playing = self.kodi.Player.GetItem([PLAYER_VIDEO])['result']['item']['label']
        if playing == '':
            playing = 'nothing is playing'
        self.properties['current_item'] = playing

    def check_connection(self, ip):
        self.kodi = Kodi('http://' + ip + '/jsonrpc')
        try:
            self.kodi.JSONRPC.Ping()
            return self.kodi
        except:
            return False

    def get_movies(self):
        self.kodi.VideoLibrary.GetMovies()

    def left(self):
        self.kodi.Input.Left()

    def right(self):
        self.kodi.Input.Right()

    def up(self):
        self.kodi.Input.Up()

    def down(self):
        self.kodi.Input.Down()

    def back(self):
        self.kodi.Input.Back()

    def info(self):
        self.kodi.Input.Info()

    def select(self):
        self.kodi.Input.Select()

    def volume_up(self):
        volume = self.kodi.Application.GetProperties({'properties': ['volume']})['result']['volume']
        volume += 5
        if volume > 100:
            volume = 100
        self.kodi.Application.SetVolume({'volume': volume})

    def volume_down(self):
        volume = self.kodi.Application.GetProperties({'properties': ['volume']})['result']['volume']
        volume -= 5
        if volume < 0:
            volume = 0
        self.kodi.Application.SetVolume({'volume': volume})

    def playpause(self):
        self.kodi.Player.PlayPause([PLAYER_VIDEO])

    def stop(self):
        self.kodi.Player.Stop([PLAYER_VIDEO])

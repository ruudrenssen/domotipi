import configparser
from kodijson import Kodi

config = configparser.ConfigParser()
config.read('config.ini')

ip = config['KODI']['IP_ADDRESS']

kodi = Kodi('http://' + ip + '/jsonrpc')

def getMovies():
    movieList = kodi.VideoLibrary.GetMovies()
    print(movieList)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from constants import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import json
import logging
import colorlog
from utilities import track_list, refresh_tracks

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(asctime)s - %(log_color)s%(levelname)s%(reset)s - %(message)s',
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
))

logger = colorlog.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

scope = 'user-library-read'

counter = 0

auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

filename = 'spotify_tracks.json'

logger.info("Загрузка треков из Spotify...")
spotify_tracks = track_list(filename)


results = sp.current_user_saved_tracks()
res_tracks = []
while results['next']:
    results = sp.next(results)
    res_tracks.append(refresh_tracks(results, spotify_tracks, filename, 'spotify'))


with open(filename, 'w', encoding='utf-8') as file:
    json.dump(spotify_tracks, file, ensure_ascii=False, indent=4)
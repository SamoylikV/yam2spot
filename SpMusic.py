import spotipy
from spotipy.oauth2 import SpotifyOAuth
from constants import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import json
import os
import logging
import colorlog

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
if os.path.exists(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        spotify_tracks = json.load(file)
else:
    spotify_tracks = []


def track_exists(artist_name, track_name):
    for track in spotify_tracks:
        if track['artist'] == artist_name and track['track_name'] == track_name:
            return True
    return False


def refresh_tracks(results):
    global counter
    for item in results['items']:
        track = item['track']
        artist_name = track['artists'][0]['name']
        track_name = track['name']
        if not track_exists(artist_name, track_name):
            counter += 1
            logger.info(f"Добавление трека {track_name} исполнителя {artist_name} в список.")
            spotify_tracks.append({'artist': artist_name, 'track_name': track_name})


results = sp.current_user_saved_tracks()
refresh_tracks(results)

while results['next']:
    results = sp.next(results)
    refresh_tracks(results)
if counter == 0:
    logger.info("Треки не обновлены.")
else:
    with open(filename, 'w', encoding='utf-8') as file:
        logger.info(f"Сохранение треков в {filename}...")
        json.dump(spotify_tracks, file, ensure_ascii=False, indent=4)

    logger.info(f"Добавлено {counter} треков.")

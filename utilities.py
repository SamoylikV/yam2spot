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


def track_exists(artist_name, track_name, tracks):
    for track in tracks:
        if track['artist'] == artist_name and track['track_name'] == track_name:
            return True
    return False


def track_list(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            tracks = json.load(file)
    else:
        tracks = []
    return tracks

def refresh_tracks(results, tracks, filename, platform):
    logger_config()
    counter = 0
    if platform == 'spotify':
        for item in results['items']:
            track = item['track']
            artist_name = track['artists'][0]['name']
            track_name = track['name']
            if not track_exists(artist_name, track_name, tracks):
                counter += 1
                logger.info(f"Добавление трека {track_name} исполнителя {artist_name} в список.")
                tracks.append({'artist': artist_name, 'track_name': track_name})
        return tracks
    elif platform == 'yandex':
        for track in results:
            if track.type != 'music':
                logger.info(f"Трек {track.title} не является музыкой.")
                continue
            try:
                artist_name = track.artists[0].name
            except:
                logger.error(f"Ошибка не удалось получить имя исполнителя для трека {track.title}.")
                continue
            track_name = track.title
            if not track_exists(artist_name, track_name, tracks):
                counter += 1
                logger.info(f"Добавление трека {track_name} исполнителя {artist_name} в список.")
                tracks.append({'artist': artist_name, 'track_name': track_name})
        if counter == 0:
            logger.info("Треки не обновлены.")
        else:
            with open(filename, 'w', encoding='utf-8') as file:
                logger.info(f"Сохранение треков в {filename}...")
                json.dump(tracks, file, ensure_ascii=False, indent=4)
            logger.info(f"Добавлено {counter} треков.")
from yandex_music import Client
from constants import YA_TOKEN
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


client = Client(YA_TOKEN).init()
tracks = client.users_likes_tracks().fetchTracks()

filename = 'yandex_tracks.json'
yandex_tracks = track_list(filename)
refresh_tracks(tracks, yandex_tracks, filename, 'yandex')
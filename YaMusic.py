from yandex_music import Client
from constants import YA_TOKEN
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


client = Client()
client = Client(YA_TOKEN).init()
client.users_likes_tracks()[0].fetch_track()
tracks = client.users_likes_tracks().fetchTracks()

for track in tracks:
    artists = track.artists
    if len(artists) > 1:
        artists = ', '.join([artist.name for artist in artists])
    else:
        artists = artists[0].name
    title = track.title
    print(title)
    # print(track.artistsName, '-', track.title)


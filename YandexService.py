from yandex_music import Client
from constants import YA_TOKEN
from utilities import TrackManager, LoggerSetup


class YandexService:
    def __init__(self):
        self.client = Client(YA_TOKEN).init()
        self.logger = LoggerSetup.setup_logger()

    def fetch_and_refresh_tracks(self):
        self.logger.info("Загрузка треков из Яндекс Музыки...")
        filename = 'yandex_tracks.json'
        track_manager = TrackManager(filename)
        liked_tracks = self.client.users_likes_tracks().fetchTracks()
        track_manager.refresh_tracks(liked_tracks, 'yandex')

        self.logger.info("Треки Яндекс Музыки обновлены.")

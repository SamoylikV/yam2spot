from utilities import TrackManager, LoggerSetup, get_diff
from SpotifyService import SpotifyService
from YandexService import YandexService


class MusicService:
    def __init__(self, desynchronize: bool = False, remove_yandex: bool = False):
        self.yandex = YandexService()
        self.spotify = SpotifyService()
        self.track_manager = TrackManager
        self.removed_tracks = TrackManager().removed_tracks
        self.ya_client = self.yandex.client
        self.sp_client = self.spotify.client
        self.yandex_tracks = TrackManager('yandex_tracks.json').load_tracks()
        self.spotify_tracks = TrackManager('spotify_tracks.json').load_tracks()
        self.logger = LoggerSetup.setup_logger()
        self.desynchronize = desynchronize
        self.remove_yandex = remove_yandex

    def sync_tracks(self):
        self.logger.info("Синхронизация треков...")
        spotify_like = get_diff(self.yandex_tracks, self.spotify_tracks)
        yandex_like = get_diff(self.spotify_tracks, self.yandex_tracks)
        self.logger.info(f"Добавление {len(spotify_like)} треков в Spotify...")

        self.spotify.add_to_spotify(spotify_like)
        if self.remove_yandex:
            self.logger.info(f"Удаление {len(self.removed_tracks)} треков из Яндекс Музыки...")
            self.yandex.delete_from_yandex(self.removed_tracks)
        if not self.desynchronize:
            self.logger.info(f"Добавление {len(yandex_like)} треков в Яндекс Музыку...")
            self.yandex.add_to_yandex(yandex_like)
        else:
            self.logger.info("Десинхронизация включена. Треки не будут добавлены в Яндекс Музыку.")
        self.logger.info("Синхронизация завершена.")

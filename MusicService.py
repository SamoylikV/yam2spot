from yandex_music import Client
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from typing import List, Dict
from constants import YA_TOKEN, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from utilities import TrackManager, LoggerSetup, get_diff


class MusicService:
    def __init__(self, desynchronize: bool = False):
        self.ya_client = Client(YA_TOKEN).init()
        self.sp_client = self._init_spotify_client()
        self.logger = LoggerSetup.setup_logger()
        self.desynchronize = desynchronize

    def _init_spotify_client(self) -> spotipy.Spotify:
        auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=SPOTIPY_REDIRECT_URI, scope='user-library-modify', cache_path=".cache")
        return spotipy.Spotify(auth_manager=auth_manager)

    def sync_tracks(self):
        yandex_tracks = TrackManager('yandex_tracks.json').load_tracks()
        spotify_tracks = TrackManager('spotify_tracks.json').load_tracks()

        self.logger.info("Синхронизация треков...")
        spotify_like = get_diff(yandex_tracks, spotify_tracks)
        yandex_like = get_diff(spotify_tracks, yandex_tracks)
        self.logger.info(f"Добавление {len(spotify_like)} треков в Spotify...")
        self._add_to_spotify(spotify_like)
        if not self.desynchronize:
            self.logger.info(f"Добавление {len(yandex_like)} треков в Яндекс Музыку...")
            self._add_to_yandex(yandex_like)
        else:
            self.logger.info("Десинхронизация включена. Треки не будут добавлены в Яндекс Музыку.")
        self.logger.info("Синхронизация завершена.")

    def _add_to_spotify(self, tracks: List[Dict]):
        for track in tracks:
            try:
                track_info = \
                    self.sp_client.search(q=f"{track['artist']} {track['track_name']}", type='track')['tracks'][
                        'items'][0]
                track_id = track_info['id']
                self.sp_client.current_user_saved_tracks_add([track_id])
            except IndexError:
                self.logger.warning(f'Трек {track["track_name"]} исполнителя {track["artist"]} не найден на Spotify.')

    def _add_to_yandex(self, tracks: List[Dict]):
        for track in tracks:
            try:
                search_result = self.ya_client.search(f"{track['artist']} {track['track_name']}")
                track_id = search_result.tracks[0].id
                if not self.desynchronize:
                    self.ya_client.users_likes_tracks_add(track_id)
            except IndexError:
                self.logger.warning(
                    f"Трек {track['track_name']} исполнителя {track['artist']} не найден на Яндекс Музыке.")

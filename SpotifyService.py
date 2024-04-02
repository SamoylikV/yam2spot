import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from constants import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
from utilities import TrackManager, LoggerSetup


class SpotifyService:
    def __init__(self):
        self.scope = 'user-library-read'
        self.sp = self._init_spotify_client()
        self.logger = LoggerSetup.setup_logger()

    def _init_spotify_client(self) -> spotipy.Spotify:
        auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=SPOTIPY_REDIRECT_URI, scope=self.scope)
        return spotipy.Spotify(auth_manager=auth_manager)

    def fetch_and_refresh_tracks(self):
        self.logger.info("Загрузка треков из Spotify…")
        filename = 'spotify_tracks.json'
        track_manager = TrackManager(filename)
        spotify_tracks = track_manager.load_tracks()

        results = self.sp.current_user_saved_tracks()
        while results['next']:
            results = self.sp.next(results)
            spotify_tracks += track_manager.refresh_tracks(results, 'spotify')

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(spotify_tracks, file, ensure_ascii=False, indent=4)
        self.logger.info("Треки Spotify обновлены.")

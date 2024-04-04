import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from constants import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, PROXIES, PLAYLIST_ID
from utilities import TrackManager, LoggerSetup
from typing import List, Dict


class SpotifyService:
    def __init__(self):
        self.scope = 'user-library-read,user-library-modify,playlist-modify-public'
        self.client = self._init_spotify_client()
        self.logger = LoggerSetup.setup_logger()
        self.removed_tracks = []

    def _init_spotify_client(self) -> spotipy.Spotify:
        auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=SPOTIPY_REDIRECT_URI, proxies=PROXIES, open_browser=False,
                                    scope=self.scope, cache_path=".cache")
        return spotipy.Spotify(auth_manager=auth_manager, proxies=PROXIES)

    def fetch_and_refresh_tracks(self):
        self.logger.info("Загрузка треков из Spotify…")
        filename = 'spotify_tracks.json'
        track_manager = TrackManager(filename)
        liked_tracks = []
        results = self.client.current_user_saved_tracks()
        counter = 0
        while results['next']:
            counter += 1
            self.logger.info(f"Загрузка страницы {counter}...")
            liked_tracks.extend(results['items'])
            results = self.client.next(results)
        track_manager.refresh_tracks(liked_tracks, 'spotify')

    def add_to_spotify(self, tracks: List[Dict]):
        for track in tracks:
            try:
                track_info = \
                    self.client.search(q=f"{track['artist']} {track['track_name']}", type='track')['tracks'][
                        'items'][0]
                track_id = track_info['id']
                self.client.current_user_saved_tracks_add([track_id])
                self.client.playlist_add_items(playlist_id=PLAYLIST_ID, items=[track_id])
            except IndexError:
                self.logger.warning(f'Трек {track["track_name"]} исполнителя {track["artist"]} не найден на Spotify.')

        self.remove_duplicates()

    def remove_duplicates(self):
        self.logger.info("Удаление дубликатов...")
        liked_tracks = []
        deleted_track_ids = []
        results = self.client.current_user_saved_tracks()
        counter = 0
        while results['next']:
            liked_tracks.extend(results['items'])
            results = self.client.next(results)

        for i in range(len(liked_tracks) - 1, -1, -1):
            track_id = liked_tracks[i]['track']['id']
            if track_id not in deleted_track_ids:
                for j in range(i - 1, -1, -1):
                    if track_id == liked_tracks[j]['track']['id']:
                        counter += 1
                        self.client.current_user_saved_tracks_delete([track_id])
                        deleted_track_ids.append(
                            {'id': track_id, 'artist': liked_tracks[j]['track']['artists'][0]['name'],
                             'track_name': liked_tracks[j]['track']['name']})
                        break
        if counter > 0:
            self.logger.info(f"Удалено {counter} дубликатов.")
            with open('deleted_spotify_tracks.json', 'w', encoding='utf-8') as f:
                json.dump(deleted_track_ids, f, ensure_ascii=False, indent=4)
        else:
            self.logger.info("Дубликатов не найдено.")

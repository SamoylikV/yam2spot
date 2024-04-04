from yandex_music import Client
from constants import YA_TOKEN
from utilities import TrackManager, LoggerSetup
from typing import List, Dict
import json


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

    def add_to_yandex(self, tracks: List[Dict]):
        for track in tracks:
            try:
                search_result = self.client.search(f"{track['artist']} {track['track_name']}")
                if search_result.tracks is None:
                    self.logger.warning(
                        f"Трек {track['track_name']} исполнителя {track['artist']} не найден на Яндекс Музыке.")
                    continue
                track_id = search_result.tracks['results'][0]['id']
                self.logger.info(
                    f"Добавление трека {track['track_name']} исполнителя {track['artist']} в Яндекс Музыку...")
                self.client.users_likes_tracks_add([track_id])
            except IndexError:
                self.logger.warning(
                    f"Трек {track['track_name']} исполнителя {track['artist']} не найден на Яндекс Музыке.")
            except TypeError:
                self.logger.warning(
                    f"Трек {track['track_name']} исполнителя {track['artist']} не найден на Яндекс Музыке.")

    def delete_from_yandex(self, tracks: List[Dict]):
        deleted_tracks = []
        for track in tracks:
            try:
                try:
                    search_result = self.client.search(f"{track['artist']} {track['track_name']}")
                except Exception as e:
                    self.logger.warning(
                        f"Трек {track['track_name']} исполнителя {track['artist']} не найден на Яндекс Музыке.")
                    continue
                if search_result.tracks is None:
                    self.logger.warning(
                        f"Трек {track['track_name']} исполнителя {track['artist']} не найден на Яндекс Музыке.")
                    continue
                track_id = search_result.tracks['results'][0]['id']
                self.logger.info(
                    f"Удаление трека {track['track_name']} исполнителя {track['artist']} из Яндекс Музыки...")
                self.client.users_likes_tracks_remove([track_id])
                deleted_tracks.append({'id': track_id, 'artist': track['artist'], 'track_name': track['track_name']})
            except IndexError:
                self.logger.warning(
                    f"Трек {track['track_name']} исполнителя {track['artist']} не найден на Яндекс Музыке.")
        with open('deleted_yandex_tracks.json', 'w', encoding='utf-8') as file:
            self.logger.info(f"Удалено {len(deleted_tracks)} из Яндекс Музыки...")
            json.dump(deleted_tracks, file, ensure_ascii=False, indent=4)

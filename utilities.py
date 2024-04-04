import json
import os
from typing import List, Dict
import logging
import colorlog
from fuzzywuzzy import fuzz


class LoggerSetup:
    @staticmethod
    def setup_logger() -> logging.Logger:
        logger = colorlog.getLogger('MusicLogger')
        if not logger.handlers:
            handler = colorlog.StreamHandler()
            handler.setFormatter(colorlog.ColoredFormatter(
                '%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s',
                reset=True,
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                },
                style='%'
            ))
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)
        return logger


class TrackManager:
    def __init__(self, filename='tracks.json'):
        self.filename = filename
        self.logger = LoggerSetup.setup_logger()
        self.tracks = self.load_tracks()
        self.removed_tracks = []

    def track_exists(self, artist_name: str, track_name: str) -> bool:
        if self.tracks is not None:
            for track in self.tracks:
                if track['artist'] == artist_name and track['track_name'] == track_name:
                    return True
        return False

    def load_tracks(self) -> List[Dict]:
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                loaded_data = json.load(file)
                if isinstance(loaded_data, list):
                    tracks = loaded_data
                else:
                    tracks = []
        else:
            tracks = []
        return tracks

    def refresh_tracks(self, results: List[Dict], platform: str):
        counter = 0
        if platform == 'spotify':
            self.removed_tracks = self.get_removed_tracks(results)
            for track_ in results:
                track = track_['track']
                artist_name = track['artists'][0]['name']
                track_name = track['name']
                self.logger.info(f"Проверка трека {track_name} - {artist_name}...")
                if not self.track_exists(artist_name, track_name):
                    self.logger.info(f"Добавляем трек {track_name} - {artist_name}.")
                    self.tracks.append({'artist': artist_name, 'track_name': track_name})
                    counter += 1
        elif platform == 'yandex':
            for track in results:
                if track['type'] != 'music':
                    self.logger.info(f"Трек {track['title']} не является музыкой.")
                    continue
                try:
                    artist_name = track['artists'][0]['name']
                    track_name = track['title']
                    if not self.track_exists(artist_name, track_name):
                        self.logger.info(f"Добавление трека {track_name} исполнителя {artist_name} в список.")
                        self.tracks.append({'artist': artist_name, 'track_name': track_name})
                        counter += 1
                except KeyError as e:
                    self.logger.error(f"Ошибка: не удалось обработать трек {track['title']}: {e}")

        if counter > 0:
            with open(self.filename, 'w', encoding='utf-8') as file:
                self.logger.info(f"Сохранение {counter} треков в {self.filename}...")
                json.dump(self.tracks, file, ensure_ascii=False, indent=4)

    def get_removed_tracks(self, results: List[Dict]) -> List[Dict]:
        removed_tracks = []
        if len(self.tracks) > len(results):
            for track in self.tracks:
                is_removed = True
                for result in results:
                    if track['track_name'] == result['track']['name'] and track['artist'] == \
                            result['track']['artists'][0]['name']:
                        is_removed = False
                        break
                if is_removed:
                    removed_tracks.append(track)
        return removed_tracks


def get_diff(tracks1: List[Dict], tracks2: List[Dict]) -> List[Dict]:
    diff = []

    for track1 in tracks1:
        track_name1_lower = track1['track_name'].lower()
        is_unique = True
        for track2 in tracks2:
            track_name2_lower = track2['track_name'].lower()
            track_name_similarity = fuzz.ratio(track_name1_lower, track_name2_lower)
            if track_name_similarity >= 70:
                is_unique = False
                break
        if is_unique:
            diff.append(track1)
    return diff

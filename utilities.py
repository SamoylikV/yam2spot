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
    def __init__(self, filename: str):
        self.filename = filename
        self.logger = LoggerSetup.setup_logger()

    @staticmethod
    def track_exists(artist_name: str, track_name: str, tracks: List[Dict]) -> bool:
        for track in tracks:
            if track['artist'] == artist_name and track['track_name'] == track_name:
                return True
        return False

    def load_tracks(self) -> List[Dict]:
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                tracks = json.load(file)
                if not tracks:
                    tracks = []
        else:
            tracks = []
        return tracks

    def refresh_tracks(self, results: List[Dict], platform: str):
        tracks = self.load_tracks()
        counter = 0
        if platform == 'spotify':
            for item in results['items']:
                track = item['track']
                artist_name = track['artists'][0]['name']
                track_name = track['name']
                if not self.track_exists(artist_name, track_name, tracks):
                    counter += 1
                    self.logger.info(f"Добавляем трек {track_name} - {artist_name}.")
                    tracks.append({'artist': artist_name, 'track_name': track_name})
            return tracks
        elif platform == 'yandex':
            for track in results:
                if track.type != 'music':
                    self.logger.info(f"Трек {track.title} не является музыкой.")
                    continue
                try:
                    artist_name = track.artists[0].name
                except:
                    self.logger.error(f"Ошибка не удалось получить имя исполнителя для трека {track.title}.")
                    continue
                track_name = track.title
                if not self.track_exists(artist_name, track_name, tracks):
                    counter += 1
                    self.logger.info(f"Добавление трека {track_name} исполнителя {artist_name} в список.")
                    tracks.append({'artist': artist_name, 'track_name': track_name})
            if counter == 0:
                self.logger.info("Треки не обновлены.")
            else:
                with open(self.filename, 'w', encoding='utf-8') as file:
                    self.logger.info(f"Сохранение треков в {self.filename}...")
                    json.dump(tracks, file, ensure_ascii=False, indent=4)
                self.logger.info(f"Добавлено {counter} треков.")

            if counter > 0:
                with open(self.filename, 'w', encoding='utf-8') as file:
                    json.dump(tracks, file, ensure_ascii=False, indent=4)
                self.logger.info(f"Добавлено {counter} треков.")


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

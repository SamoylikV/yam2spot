import inquirer
import time
import schedule
from MusicService import MusicService
from YandexService import YandexService
from SpotifyService import SpotifyService
from utilities import LoggerSetup


def job():
    logger = LoggerSetup.setup_logger()
    logger.info("Запуск синхронизации треков...")
    yandex_music = YandexService()
    yandex_music.fetch_and_refresh_tracks()
    spotify_music = SpotifyService()
    spotify_music.fetch_and_refresh_tracks()
    music_service = MusicService(desynchronize)
    music_service.sync_tracks()
    logger.info("До следующей синхронизации осталось 1 час.")


def run_once():
    job()


def run_hourly():
    schedule.every().hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    questions = [
        inquirer.List('mode',
                      message="Выберите режим запуска скрипта",
                      choices=['Единоразово', 'Каждый час'],
                      ),
        inquirer.List('desynchronize',
                      message="Добавлять треки из Spotify в Яндекс Музыку?",
                      choices=['Да', 'Нет'],
                      ),
    ]
    answers = inquirer.prompt(questions)
    if answers['desynchronize'] == 'Да':
        desynchronize = False
    else:
        desynchronize = True
    if answers['mode'] == 'Единоразово':
        run_once()
    else:
        run_hourly()

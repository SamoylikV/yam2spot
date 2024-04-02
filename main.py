from MusicService import MusicService
from YandexService import YandexService
from SpotifyService import SpotifyService

if __name__ == "__main__":
    yandex_music = YandexService()
    yandex_music.fetch_and_refresh_tracks()
    spotify_music = SpotifyService()
    spotify_music.fetch_and_refresh_tracks()
    music_service = MusicService()
    music_service.sync_tracks()

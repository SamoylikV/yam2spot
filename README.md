# Синхронизация музыкальных сервисов

Проект предназначен для синхронизации музыкальных треков между различными музыкальными сервисами, такими как Spotify и Яндекс Музыка.

## Функциональность

- Аутентификация в музыкальных сервисах Spotify и Яндекс Музыка.
- Извлечение списка любимых треков пользователя из каждого сервиса.
- Синхронизация избранных треков между сервисами.

## Структура проекта

- `constants.py` - содержит константы для аутентификации в музыкальных сервисах.
- `main.py` - основной исполняемый файл проекта, запускающий процесс синхронизации.
- `MusicService.py` - определяет базовый класс для работы с музыкальными сервисами.
- `SpotifyService.py` и `YandexService.py` - модули для работы со специфическими API Spotify и Яндекс Музыка соответственно.
- `utilities.py` - вспомогательные утилиты, включая логирование и управление треками.
- `requirements.txt` - список зависимостей Python, необходимых для работы приложения.

## Установка

Для работы с проектом необходим Python версии 3.6 или выше. Установите зависимости проекта, используя следующую команду:

```
pip install -r requirements.txt
```

## Настройка

Перед использованием необходимо настроить аутентификационные данные для каждого музыкального сервиса в файле `constants.py`:

- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`
- `YA_TOKEN`

## Запуск

Запустите проект, используя команду:

```
python main.py
```

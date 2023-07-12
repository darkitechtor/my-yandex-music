import os

from progress.bar import Bar
from time import sleep

from yandex_music import Client

# токен для авторизаци в ЯМ
TOKEN = os.environ.get('TOKEN')

# DEBUG: на время разработки усечем списки для более высокой скорости работы
DEBUG_LIST_CUT = slice(0,2)

# инициируем клиент ЯМ
client = Client(TOKEN).init()

"""ПОЛУЧЕНИЕ СПИСКОВ ЛАЙКОВ ПО ИСПОЛНИТЕЛЯМ, АЛЬБОМАМ И ПЕСНЯМ"""

# получаем список id лайкнутых исполнителей
artists = client.users_likes_artists()
artist_ids = []
try:
    for artist in artists:
        artist_ids.append(artist.artist.id)
except: # type: ignore
    print("Artists weren't loaded.")
#    exit() # в Jupyter лучше не прерывать код
else:
    print("Artists were loaded.")

# получаем список id лайкнутых альбомов
albums = client.users_likes_albums(rich=False)
album_ids = []
try:
    for album in albums:
        album_ids.append(album['id'])
except: # type: ignore
    print("Albums weren't loaded.")
#    exit() # в Jupyter лучше не прерывать код
else:
    print("Albums were loaded.")

# получаем список id лайкнутых песен
tracks = client.users_likes_tracks()
track_ids = []
try:
    for track in tracks.tracks_ids:
        track_ids.append(track)
except: # type: ignore
    print("Tracks weren't loaded.")
#    exit() # в Jupyter лучше не прерывать код
else:
    print("Tracks were loaded.")

""" ПОЛУЧАЕМ ПО КАЖДОЙ СУЩНОСТИ ДАННЫЕ, НЕОБХОДИМЫЕ ДЛЯ БАЗЫ ЗНАНИЙ """

liked_artists = []
liked_albums = []
liked_tracks = []

# получаем список информации по лайкнутым исполнителям, перебирая их id
with Bar('Processing artists...') as bar:
    for artist_id in artist_ids:
        artist_data = {}
        artists = client.artists(artist_id)

        for artist in artists:
            artist_data["name"] = artist.name
            artist_data["countries"] = artist.countries
            artist_data["genres"] = artist.genres

            liked_artists.append(artist_data)

        sleep(1)
        bar.next()

# получаем список информации по лайкнутым альбомам, перебирая их id
# TODO потом по лайкнутым нужно проставлять 3/5 звезд, а по остальным 5+5 звезд.
with Bar('Processing albums...') as bar:
    for album_id in album_ids:
        album_data = {}
        albums = client.albums(album_id)

        for album in albums:
            album_data["title"] = album.title
            album_data["artists"] = [artist.name for artist in album.artists]
            album_data["year"] = album.year

            liked_albums.append(album_data)

        sleep(1)
        bar.next()

# получаем список информации по лайкнутым песням, перебирая их id
with Bar('Processing tracks...') as bar:
    for track_id in track_ids:
        track_data = {}
        tracks = client.tracks(track_id)

        for track in tracks:
            track_data["title"] = track.title
            track_data["artists"] = [artist.name for artist in track.artists]

            liked_tracks.append(track_data)

        sleep(1)
        bar.next()

# print(liked_artists)
# print(liked_albums)
# print(liked_tracks)

with open("result.txt", "w") as f:
	f.write(liked_artists)
with open("result.txt", "a") as f:
	f.write(liked_albums)
with open("result.txt", "a") as f:
	f.write(liked_tracks)
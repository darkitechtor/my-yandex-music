import os

from tqdm import tqdm
from time import sleep

from yandex_music import Client

# токен для авторизаци в ЯМ
TOKEN = os.environ.get('TOKEN')

# DEBUG: на время разработки усечем списки для более высокой скорости работы
# DEBUG_LIST_CUT = slice(0,10)

# инициируем клиент ЯМ
client = Client(TOKEN).init()

"""
ПОЛУЧЕНИЕ СПИСКОВ ЛАЙКОВ ПО ИСПОЛНИТЕЛЯМ, АЛЬБОМАМ И ПЕСНЯМ
"""

# получаем список id лайкнутых исполнителей
artists = client.users_likes_artists()
artist_ids = []
try:
    for artist in artists:
        artist_ids.append(artist.artist.id)
except: # type: ignore
    print("Artists weren't loaded.")
    exit()
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
    exit()
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
    exit()
else:
    print("Tracks were loaded.")

"""
ПОЛУЧАЕМ ПО КАЖДОЙ СУЩНОСТИ ДАННЫЕ, НЕОБХОДИМЫЕ ДЛЯ БАЗЫ ЗНАНИЙ
"""

liked_albums = []
liked_tracks = []
liked_artists = []

# получаем список информации по лайкнутым альбомам, перебирая их id
for album_id in tqdm(album_ids, desc="Liked Albums"):
    album_data = {}
    albums = client.albums(album_id)

    for album in albums:
        album_data["title"] = album.title
        album_data["artists"] = [artist.name for artist in album.artists]
        album_data["year"] = album.year
        album_data["rate"] = '★★★☆☆'

        liked_albums.append(album_data)

        for artist in album.artists:
            artist_ids.append(artist.id)

    sleep(0.5)

with open("liked_albums.txt", "w") as f:
	f.write(liked_albums)

# получаем список информации по лайкнутым песням, перебирая их id
for track_id in tqdm(track_ids, desc="Tracks"):
    track_data = {}
    tracks = client.tracks(track_id)

    for track in tracks:
        track_data["title"] = track.title
        track_data["artists"] = [artist.name for artist in track.artists]

        liked_tracks.append(track_data)

        for artist in track.artists:
            artist_ids.append(artist.id)

    sleep(0.5)

with open("liked_tracks.txt", "w") as f:
	f.write(liked_tracks)

# получаем список информации по лайкнутым исполнителям, перебирая их id
for artist_id in tqdm(artist_ids, desc="Artists"):
    artist_data = {}
    artists = client.artists(artist_id)

    for artist in artists:
        artist_data["name"] = artist.name
        artist_data["countries"] = artist.countries
        artist_data["genres"] = artist.genres

        liked_artists.append(artist_data)

    sleep(0.5)

with open("liked_artists.txt", "w") as f:
	f.write(liked_artists)

# чтобы список исполнителей был полным, выполняем этот шаг сейчас,
# а не в предыдущем блоке
# получаем список id альбомов лайкнутых артистов
all_album_ids = []
try:
    for artist in tqdm(list(set(artist_ids)), desc="All Albums"):
        all_albums = client.artists_direct_albums(artist)
        for album in all_albums:
            all_album_ids.append(album['id'])

        sleep(0.5)
except: # type: ignore
    print("All albums weren't loaded.")
    exit()
else:
    print("All albums were loaded.")
        
# получаем список информации по всем альбомам лайкнутых исполнителей,
# перебирая их id

all_albums = []

for album_id in tqdm(list(filter(lambda x: x not in album_ids,
                                 all_album_ids
                                 ))):
    album_data = {}
    albums = client.albums(album_id)

    for album in albums:
        album_data["title"] = album.title
        album_data["artists"] = [artist.name for artist in album.artists]
        album_data["year"] = album.year
        album_data["rate"] = '★★★★★☆☆☆☆☆'

        all_albums.append(album_data)

    sleep(0.5)

with open("all_albums.txt", "w") as f:
	f.write(all_albums)

"""
ЗАПИСЫВАЕМ ДАННЫЕ В ФАЙЛЫ В НУЖНОМ ФОРМАТЕ
"""

# исполнители
for artist in tqdm(liked_artists, desc="Artists"):
    if artist["countries"] is not None:
        countries = artist["countries"]
    else:
        countries = ["<>"]
    with open(f"result/{artist['name']}.md", "w") as f:
        f.write(
            f"""---
genre: {", ".join(i for i in artist["genres"])}
country: {", ".join(i for i in countries)}
---

|Album|Year|Rate|Comments|
|-|-|-|-|"""
            )
        
# все альбомы
for album in tqdm(all_albums, desc="All Albums"):
    with open(f"result/{album['artists'][0]}.md", "a") as f:
        f.write(
            f"""
|{album["title"]}|{album["year"]}|{album["rate"]}||"""
            )
        
# лайкнутые альбомы
for album in tqdm(liked_albums, desc="Liked Albums"):
    with open(f"result/{album['artists'][0]}.md", "a") as f:
        f.write(
            f"""
|{album["title"]}|{album["year"]}|{album["rate"]}||"""
            )
        
# допишем заголовок для любимых песен
for artist in tqdm(liked_artists, desc="Tracks Headings"):
    with open(f"result/{artist['name']}.md", "a") as f:
        f.write(
            f"""
Favourite songs:
"""
            )
        
# лайкнутые песни
for track in tqdm(liked_tracks, desc="Tracks"):
    with open(f"result/{track['artists'][0]}.md", "a") as f:
        f.write(
            f"""
- {track["title"]}"""
            )
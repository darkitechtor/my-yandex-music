import os

from yandex_music import Client

# без авторизации недоступен список треков альбома
TOKEN = os.environ.get('TOKEN')

# на время разработки усечем списки для более высокой скорости работы
DEBUG_LIST_CUT = slice(0,2)

client = Client(TOKEN).init()

# получаем список лайкнутых альбомов (их id)
albums = client.users_likes_albums(rich=False)
album_ids = []
for album in albums:
    album_ids.append(album['id'])

# получаем список информации по лайкнутым альбомам, перебирая их id
for album_id in album_ids[DEBUG_LIST_CUT]:
    album = client.albums_with_tracks(album_id)
    tracks = []
    for i, volume in enumerate(album.volumes):
        if len(album.volumes) > 1:
            tracks.append(f'💿 Диск {i + 1}')
        tracks += volume

    text = 'АЛЬБОМ\n\n'
    text += f'{album.title}\n'
    text += f"Исполнитель: {', '.join([artist.name for artist in album.artists])}\n"
    text += f'{album.year} · {album.genre}\n'

    cover = album.cover_uri
    if cover:
        text += f'Обложка: {cover.replace("%%", "400x400")}\n\n'

    text += 'Список треков:'

    print(text)

    for track in tracks:
        if isinstance(track, str):
            print(track)
        else:
            artists = ''
            if track.artists:
                artists = ' - ' + ', '.join(artist.name for artist in track.artists)
            print(track.title + artists)
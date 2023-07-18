def file_beautifier(file):
    # определяем границы блоков для корректного разнесения по переменным
    with open(file, "r") as f:
        albums_start_line = 0
        albums_end_line = 0
        tracks_start_line = 0
        i = 0
        for line in f.readlines():
            if line[:7] == "|Album|":
                albums_start_line = i+2
            elif line[:9] == "Favourite":
                albums_end_line = i-1
                tracks_start_line = i+1
            i += 1

    # записываем блоки в переменные для работы с ними и сохранения
    with open(file, "r") as f:
        albums = f.readlines()[albums_start_line:albums_end_line]

    with open(file, "r") as f:
        tracks = f.readlines()[tracks_start_line:]

    with open(file, "r") as f:
        heading = f.readlines()[:albums_start_line]

    """
    **ЗАДАЧИ**
    в альбомах:
    удалить дубликаты
    вычленить год и название - для сортировки
    """

    # избавляемся от дубликатов
    albums = list(set(albums))

    # вычленяем необходимые для сортировки параметры и записываем в новый список
    albums_parsed = []
    for album in albums:
        albums_dict = {}
        albums_dict["row"] = album
        albums_dict["title"] = album.split("|")[1]
        albums_dict["year"] = album.split("|")[2]
        albums_parsed.append(albums_dict)

    albums_parsed = sorted(albums_parsed, key=lambda x: (x["year"], x["title"]))

    """
    **ЗАДАЧИ**
    в треках:
    убрать '\n', удалить дубликаты и собрать обратно, добавив '\n'
    """
    tracks_cleared = []

    # очищаем строки от '\n', иначе дубли корректно не обработаются
    for track in tracks:
        track = track.replace("\n", "").replace("*", "-")
        tracks_cleared.append(track)

    # избавляемся от дубликатов
    tracks_cleared = list(set(tracks_cleared))

    """
    ЗАПИСЬ В ФАЙЛ
    """
    with open(file, "w") as f:
        for row in heading:
            f.write(row)

    with open(file, "a") as f:
        for album in albums_parsed:
            f.write(album["row"])

    with open(file, "a") as f:
        f.write(
            """

Favourite songs:
"""
        )

    with open(file, "a") as f:
        for track in tracks_cleared:
            f.write(track + "\n")
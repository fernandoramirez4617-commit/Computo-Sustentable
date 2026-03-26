from spot import search_artist, search_track, get_artist_albums, get_album_tracks


def format_time(seconds: int) -> str:
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


def mostrar_artistas(artists):
    print("\n=== ARTISTAS ENCONTRADOS ===")
    for i, artist in enumerate(artists, start=1):
        name = artist.get("name", "Sin nombre")
        fans = artist.get("nb_fan", "N/A")
        artist_id = artist.get("id", "N/A")
        print(f"{i}. {name} | fans: {fans} | id: {artist_id}")


def elegir_artista():
    artist_name = input("\nEscribe el nombre del artista: ").strip()

    if not artist_name:
        print("No escribiste ningún artista.")
        return None

    artists = search_artist(artist_name, limit=10)

    if not artists:
        print("No se encontraron artistas.")
        return None

    mostrar_artistas(artists)

    while True:
        opcion = input("\nSelecciona un artista por número (o 0 para cancelar): ").strip()

        if not opcion.isdigit():
            print("Debes escribir un número.")
            continue

        opcion = int(opcion)

        if opcion == 0:
            return None

        if 1 <= opcion <= len(artists):
            return artists[opcion - 1]

        print("Número inválido.")


def mostrar_albums(albums):
    print("\n=== ÁLBUMES ===")
    for i, album in enumerate(albums, start=1):
        title = album.get("title", "Sin título")
        release_date = album.get("release_date", "Fecha desconocida")
        nb_tracks = album.get("nb_tracks", "N/A")
        print(f"{i}. {title} | fecha: {release_date} | canciones: {nb_tracks}")


def elegir_album(artist):
    albums = get_artist_albums(artist["id"], limit=100)

    if not albums:
        print("No se encontraron álbumes para este artista.")
        return None

    mostrar_albums(albums)

    while True:
        opcion = input("\nSelecciona un álbum por número (o 0 para regresar): ").strip()

        if not opcion.isdigit():
            print("Debes escribir un número.")
            continue

        opcion = int(opcion)

        if opcion == 0:
            return None

        if 1 <= opcion <= len(albums):
            return albums[opcion - 1]

        print("Número inválido.")


def mostrar_tracks(album, tracks):
    print(f"\n=== CANCIONES DEL ÁLBUM: {album.get('title', 'Sin título')} ===")
    for i, track in enumerate(tracks, start=1):
        title = track.get("title", "Sin título")
        duration = track.get("duration", 0)
        print(f"{i}. {title} [{format_time(duration)}]")


def mostrar_canciones_buscadas(tracks):
    print("\n=== CANCIONES ENCONTRADAS ===")
    for i, track in enumerate(tracks, start=1):
        title = track.get("title", "Sin título")
        duration = track.get("duration", 0)

        artist_info = track.get("artist") or {}
        album_info = track.get("album") or {}

        artist_name = artist_info.get("name", "Desconocido")
        album_name = album_info.get("title", "Sin álbum")

        print(
            f"{i}. {artist_name} - {title} "
            f"({album_name}) [{format_time(duration)}]"
        )


def buscar_y_agregar_cancion(playlist):
    nombre = input("\nEscribe el nombre de la canción: ").strip()

    if not nombre:
        print("No escribiste ninguna canción.")
        return

    tracks = search_track(nombre, limit=15)

    if not tracks:
        print("No se encontraron canciones.")
        return

    mostrar_canciones_buscadas(tracks)

    while True:
        seleccion = input(
            "\nSelecciona canción por número, varios por coma (ej. 1,3,5), "
            "'*' para agregar todas, o 0 para cancelar: "
        ).strip()

        if seleccion == "0":
            return

        if seleccion == "*":
            for track in tracks:
                artist_info = track.get("artist") or {}
                album_info = track.get("album") or {}

                playlist.append({
                    "artist": artist_info.get("name", "Desconocido"),
                    "album": album_info.get("title", "Sin álbum"),
                    "title": track.get("title", "Sin título"),
                    "duration": track.get("duration", 0),
                })
            print("Se agregaron todas las canciones encontradas.")
            return

        partes = [p.strip() for p in seleccion.split(",") if p.strip()]

        if not partes:
            print("Entrada vacía.")
            continue

        numeros = []
        valido = True

        for p in partes:
            if not p.isdigit():
                valido = False
                break

            n = int(p)
            if not (1 <= n <= len(tracks)):
                valido = False
                break

            numeros.append(n)

        if not valido:
            print("Selección inválida.")
            continue

        for n in numeros:
            track = tracks[n - 1]
            artist_info = track.get("artist") or {}
            album_info = track.get("album") or {}

            playlist.append({
                "artist": artist_info.get("name", "Desconocido"),
                "album": album_info.get("title", "Sin álbum"),
                "title": track.get("title", "Sin título"),
                "duration": track.get("duration", 0),
            })

        print("Canciones agregadas correctamente.")
        return


def agregar_canciones_a_playlist(playlist, artist_name, album, tracks):
    while True:
        seleccion = input(
            "\nEscribe números separados por coma para agregar canciones "
            "(ej. 1,3,5), '*' para agregar todas, o 0 para cancelar: "
        ).strip()

        if seleccion == "0":
            return

        if seleccion == "*":
            for track in tracks:
                playlist.append({
                    "artist": artist_name,
                    "album": album.get("title", "Sin título"),
                    "title": track.get("title", "Sin título"),
                    "duration": track.get("duration", 0),
                })
            print("Se agregaron todas las canciones del álbum a la playlist.")
            return

        partes = [p.strip() for p in seleccion.split(",") if p.strip()]

        if not partes:
            print("Entrada vacía.")
            continue

        numeros = []
        valido = True

        for p in partes:
            if not p.isdigit():
                valido = False
                break

            n = int(p)
            if not (1 <= n <= len(tracks)):
                valido = False
                break

            numeros.append(n)

        if not valido:
            print("Selección inválida. Intenta otra vez.")
            continue

        for n in numeros:
            track = tracks[n - 1]
            playlist.append({
                "artist": artist_name,
                "album": album.get("title", "Sin título"),
                "title": track.get("title", "Sin título"),
                "duration": track.get("duration", 0),
            })

        print("Canciones agregadas correctamente.")
        return


def mostrar_playlist(playlist):
    print("\n=== TU PLAYLIST ===")

    if not playlist:
        print("Aún no has agregado canciones.")
        return

    total = 0

    for i, song in enumerate(playlist, start=1):
        artist = song["artist"]
        album = song["album"]
        title = song["title"]
        duration = song["duration"]
        total += duration

        print(f"{i}. {artist} - {title} ({album}) [{format_time(duration)}]")

    print(f"\nDuración total: {format_time(total)}")
    print(f"Total de canciones: {len(playlist)}")


def navegar_por_artista(playlist):
    artist = elegir_artista()
    if not artist:
        return

    artist_name = artist.get("name", "Desconocido")
    print(f"\nArtista seleccionado: {artist_name}")

    while True:
        album = elegir_album(artist)
        if not album:
            break

        tracks = get_album_tracks(album["id"])

        if not tracks:
            print("No se encontraron canciones en este álbum.")
            continue

        mostrar_tracks(album, tracks)
        agregar_canciones_a_playlist(playlist, artist_name, album, tracks)

        seguir_album = input(
            "\n¿Quieres ver otro álbum de este artista? (si/no): "
        ).strip().lower()

        if seguir_album != "si":
            break


def menu_principal():
    playlist = []

    while True:
        print("\n==============================")
        print("1. Buscar artista")
        print("2. Buscar canción")
        print("3. Ver playlist")
        print("4. Salir")
        print("==============================")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            navegar_por_artista(playlist)

        elif opcion == "2":
            buscar_y_agregar_cancion(playlist)

        elif opcion == "3":
            mostrar_playlist(playlist)

        elif opcion == "4":
            print("\nPlaylist final:")
            mostrar_playlist(playlist)
            print("\nPrograma finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_principal()
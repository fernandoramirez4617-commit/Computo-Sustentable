from spot import search_artist, search_track

MAX_CANCIONES = 10


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


def agregar_track_a_playlist(playlist, track):
    if len(playlist) >= MAX_CANCIONES:
        print(f"Error: la playlist no puede tener más de {MAX_CANCIONES} canciones.")
        return False

    artist_info = track.get("artist") or {}
    album_info = track.get("album") or {}

    playlist.append({
        "artist": artist_info.get("name", "Desconocido"),
        "album": album_info.get("title", "Sin álbum"),
        "title": track.get("title", "Sin título"),
        "duration": track.get("duration", 0),
    })
    return True


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
            if len(playlist) >= MAX_CANCIONES:
                print(f"Error: la playlist ya tiene el máximo de {MAX_CANCIONES} canciones.")
                return

            espacios_disponibles = MAX_CANCIONES - len(playlist)
            canciones_a_agregar = tracks[:espacios_disponibles]

            for track in canciones_a_agregar:
                agregar_track_a_playlist(playlist, track)

            if len(canciones_a_agregar) < len(tracks):
                print(
                    f"Error: solo se agregaron {len(canciones_a_agregar)} canciones "
                    f"porque la playlist llegó al límite de {MAX_CANCIONES}."
                )
            else:
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
            if not agregar_track_a_playlist(playlist, track):
                return

        print("Canciones agregadas correctamente.")
        return


def obtener_canciones_del_artista(artist_name):
    tracks = search_track(artist_name, limit=30)

    filtradas = []
    vistos = set()

    for track in tracks:
        artist_info = track.get("artist") or {}
        album_info = track.get("album") or {}

        nombre_artista_track = artist_info.get("name", "").strip().lower()
        nombre_artista_busqueda = artist_name.strip().lower()
        titulo = track.get("title", "Sin título").strip().lower()
        album = album_info.get("title", "Sin álbum").strip().lower()

        if nombre_artista_busqueda in nombre_artista_track:
            clave = (nombre_artista_track, titulo, album)
            if clave not in vistos:
                vistos.add(clave)
                filtradas.append(track)

    return filtradas


def navegar_por_artista(playlist):
    artist = elegir_artista()
    if not artist:
        return

    artist_name = artist.get("name", "Desconocido")
    print(f"\nArtista seleccionado: {artist_name}")

    tracks = obtener_canciones_del_artista(artist_name)

    if not tracks:
        print("No se encontraron canciones para este artista.")
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
            if len(playlist) >= MAX_CANCIONES:
                print(f"Error: la playlist ya tiene el máximo de {MAX_CANCIONES} canciones.")
                return

            espacios_disponibles = MAX_CANCIONES - len(playlist)
            canciones_a_agregar = tracks[:espacios_disponibles]

            for track in canciones_a_agregar:
                agregar_track_a_playlist(playlist, track)

            if len(canciones_a_agregar) < len(tracks):
                print(
                    f"Error: solo se agregaron {len(canciones_a_agregar)} canciones "
                    f"porque la playlist llegó al límite de {MAX_CANCIONES}."
                )
            else:
                print("Se agregaron todas las canciones.")
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
            if not agregar_track_a_playlist(playlist, track):
                return

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
    print(f"Total de canciones: {len(playlist)}/{MAX_CANCIONES}")


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
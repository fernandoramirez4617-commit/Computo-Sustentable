import requests

BASE_URL = "https://api.deezer.com"


def search_artist(artist_name: str, limit: int = 10):
    """
    Busca varios artistas por nombre.
    """
    url = f"{BASE_URL}/search/artist"
    params = {"q": artist_name, "limit": max(limit, 1)}

    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    return data.get("data", [])


def search_track(track_name: str, limit: int = 15):
    """
    Busca canciones por nombre.
    """
    url = f"{BASE_URL}/search/track"
    params = {"q": track_name, "limit": max(limit, 1)}

    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    return data.get("data", [])


def get_artist_albums(artist_id: int, limit: int = 100):
    """
    Obtiene álbumes del artista, priorizando álbumes reales
    y dejando más abajo singles o lanzamientos cortos.
    """
    url = f"{BASE_URL}/artist/{artist_id}/albums"
    params = {"limit": max(limit, 1)}

    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    albums = data.get("data", [])

    blocked_words = [
        "live",
        "remix",
        "karaoke",
        "instrumental",
        "radio edit",
        "tribute",
        "mix",
        "session",
        "sessions",
        "en vivo",
        "directo",
        "version",
        "versión",
        "acoustic",
    ]

    unique_real_albums = {}
    other_releases = []

    for album in albums:
        title = album.get("title", "").strip()
        title_lower = title.lower()

        if not title:
            continue

        if any(word in title_lower for word in blocked_words):
            continue

        nb_tracks = album.get("nb_tracks")
        release_date = album.get("release_date", "")

        item = {
            "id": album.get("id"),
            "title": title,
            "release_date": release_date,
            "nb_tracks": nb_tracks if nb_tracks is not None else "N/A",
            "raw_nb_tracks": nb_tracks if isinstance(nb_tracks, int) else 0,
            "artist": album.get("artist", {}),
        }

        # Consideramos álbum principal si tiene 6 o más canciones
        if isinstance(nb_tracks, int) and nb_tracks >= 6:
            key = title_lower
            if key not in unique_real_albums:
                unique_real_albums[key] = item
            else:
                # Si ya existe uno con el mismo título, dejamos el de más canciones
                if item["raw_nb_tracks"] > unique_real_albums[key]["raw_nb_tracks"]:
                    unique_real_albums[key] = item
        else:
            other_releases.append(item)

    real_albums = list(unique_real_albums.values())

    # Primero más canciones, luego más reciente
    real_albums.sort(
        key=lambda x: (x["raw_nb_tracks"], x["release_date"]),
        reverse=True
    )

    # Si no hay álbumes largos, como respaldo devolvemos otros lanzamientos
    if not real_albums:
        other_releases.sort(
            key=lambda x: (x["raw_nb_tracks"], x["release_date"]),
            reverse=True
        )
        return other_releases[:30]

    return real_albums[:30]


def get_album_tracks(album_id: int):
    """
    Obtiene todas las canciones de un álbum.
    """
    url = f"{BASE_URL}/album/{album_id}/tracks"

    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()

    return data.get("data", [])
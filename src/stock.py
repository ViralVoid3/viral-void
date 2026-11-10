
"""Vídeos y fotos de archivo gratuitos desde Pixabay."""
import os
import random
from pathlib import Path

import requests

API = "https://pixabay.com/api/"


def _params():
    return {"key": os.environ["PIXABAY_API_KEY"]}


def _download(url: str, path: Path):
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)


def find_video(query: str, outdir: Path, idx: int):
    """Devuelve la ruta de un clip horizontal o None si no hay."""
    if not os.getenv("PIXABAY_API_KEY"):
        return None

    outdir.mkdir(parents=True, exist_ok=True)

    try:
        r = requests.get(
            f"{API}videos/",
            params={
                **_params(),
                "q": query,
                "per_page": 8,
                "safesearch": "true",
            },
            timeout=30,
        )
        r.raise_for_status()
        videos = r.json().get("hits", [])

        if not videos:
            return None

        random.shuffle(videos)

        for v in videos[:5]:
            resolutions = v.get("videos", {})

            # Preferir alta resolución, pero aceptar 720p.
            for quality in ("large", "medium", "small"):
                video = resolutions.get(quality, {})
                url = video.get("url")
                width = video.get("width", 0)
                height = video.get("height", 0)

                if url and width >= 1280 and width > height:
                    path = outdir / f"clip_{idx:02d}.mp4"
                    _download(url, path)
                    return str(path)

        return None

    except Exception as e:
        print(f"[stock] sin clip para '{query}': {e}")
        return None


def find_photo(query: str, path: Path):
    """Devuelve la ruta de una fotografía horizontal o None."""
    if not os.getenv("PIXABAY_API_KEY"):
        return None

    try:
        r = requests.get(
            API,
            params={
                **_params(),
                "q": query,
                "image_type": "photo",
                "orientation": "horizontal",
                "per_page": 5,
                "safesearch": "true",
            },
            timeout=30,
        )
        r.raise_for_status()
        photos = r.json().get("hits", [])

        if not photos:
            return None

        photo = random.choice(photos)
        url = photo.get("largeImageURL") or photo.get("webformatURL")

        if not url:
            return None

        _download(url, path)
        return str(path)

    except Exception as e:
        print(f"[stock] sin foto para '{query}': {e}")
        return None

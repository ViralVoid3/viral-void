"""Sube el vídeo como privado con publicación programada + miniatura."""
from googleapiclient.http import MediaFileUpload

from config import CATEGORY_ID


def upload(yt, video_path: str, thumb_path: str, meta: dict, publish_at):
    tags, total = [], 0
    for t in meta.get("tags", []):
        total += len(t) + 1
        if total > 450:
            break
        tags.append(t)

    body = {
        "snippet": {
            "title": meta["title"][:100],
            "description": meta["description"][:4900],
            "tags": tags,
            "categoryId": CATEGORY_ID,
            "defaultLanguage": "es",
            "defaultAudioLanguage": "es",
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "selfDeclaredMadeForKids": False,
        },
    }
    req = yt.videos().insert(
        part="snippet,status", body=body,
        media_body=MediaFileUpload(video_path, chunksize=8 * 1024 * 1024, resumable=True),
    )
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    video_id = resp["id"]
    try:
        yt.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumb_path)).execute()
    except Exception as e:  # requiere canal verificado por teléfono
        print(f"[upload] miniatura no subida (¿canal sin verificar?): {e}")
    return video_id

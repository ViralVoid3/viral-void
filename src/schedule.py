"""Elige la hora de publicación según el rendimiento de tus propios vídeos.

Nota: la API de YouTube Analytics no ofrece datos por hora del día, así que se
usa un proxy: visualizaciones por día de tus vídeos agrupadas por hora de
publicación. Con menos de 10 vídeos se usa la hora por defecto.
"""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from config import DEFAULT_PUBLISH_HOUR, TIMEZONE

TZ = ZoneInfo(TIMEZONE)


def best_hour(yt) -> int:
    try:
        ch = yt.channels().list(part="contentDetails", mine=True).execute()
        uploads = ch["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        items = yt.playlistItems().list(
            part="contentDetails", playlistId=uploads, maxResults=50
        ).execute()["items"]
        ids = [i["contentDetails"]["videoId"] for i in items]
        if len(ids) < 10:
            return DEFAULT_PUBLISH_HOUR
        vids = yt.videos().list(part="snippet,statistics", id=",".join(ids)).execute()["items"]
        now = datetime.now(timezone.utc)
        by_hour = {}
        for v in vids:
            pub = datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
            age = (now - pub).days
            if age < 3:
                continue
            vpd = int(v["statistics"].get("viewCount", 0)) / age
            by_hour.setdefault(pub.astimezone(TZ).hour, []).append(vpd)
        ok = {h: sum(x) / len(x) for h, x in by_hour.items() if len(x) >= 2}
        return max(ok, key=ok.get) if ok else DEFAULT_PUBLISH_HOUR
    except Exception as e:
        print(f"[schedule] usando hora por defecto: {e}")
        return DEFAULT_PUBLISH_HOUR


def next_publish_time(yt=None) -> datetime:
    hour = best_hour(yt) if yt else DEFAULT_PUBLISH_HOUR
    now = datetime.now(TZ)
    target = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if target <= now + timedelta(hours=2):  # margen para revisar antes
        target += timedelta(days=1)
    return target.astimezone(timezone.utc)

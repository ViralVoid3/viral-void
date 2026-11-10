"""Orquesta todo el pipeline diario.

Uso:  python src/main.py            -> genera y sube (privado, programado)
      python src/main.py --dry-run  -> genera todo pero NO sube
"""
import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import captions
import research
import schedule
import script_gen
import stock
import thumbnail
import upload
import video
import voice
import yt_client

HISTORY = Path("data/history.json")


def load_history():
    return json.loads(HISTORY.read_text()) if HISTORY.exists() else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    day = datetime.now().strftime("%Y-%m-%d")
    out = Path("out") / day
    out.mkdir(parents=True, exist_ok=True)

    yt = yt_client.service() if yt_client.available() else None
    history = load_history()

    print("1/6 Estudio de mercado...")
    topic = research.choose_topic(history, yt)
    print("   Tema:", topic["topic"])

    print("2/6 Guion...")
    meta = script_gen.generate(topic)
    scenes = meta["scenes"]

    print("3/6 Locución...")
    voice.synth(scenes, out / "audio")

    print("4/6 Clips y subtítulos...")
    clips = []
    for i, s in enumerate(scenes):
        clips.append(stock.find_video(s["visual_query"], out / "clips", i))
        captions.render_chunks(s, out / "captions", i)

    print("5/6 Montaje...")
    final = out / "video.mp4"
    video.render(scenes, clips, out / "scenes", final)
    photo = stock.find_photo(meta["thumbnail_query"], out / "thumb_bg.jpg")
    thumb = out / "thumbnail.jpg"
    thumbnail.make(meta["thumbnail_text"], photo, thumb)

    (out / "meta.json").write_text(
        json.dumps({"topic": topic, "meta": {k: v for k, v in meta.items() if k != "scenes"}},
                   ensure_ascii=False, indent=2)
    )

    publish_at = schedule.next_publish_time(yt)
    video_id = None
    if args.dry_run or yt is None:
        print("6/6 Sin subida (dry-run o faltan credenciales de YouTube).")
    else:
        print("6/6 Subiendo...")
        video_id = upload.upload(yt, str(final), str(thumb), meta, publish_at)
        print(f"   Subido: https://studio.youtube.com/video/{video_id}/edit "
              f"(se publica {publish_at.isoformat()})")

    if not args.dry_run:
        history.append({"date": day, "topic": topic["topic"], "title": meta["title"],
                        "video_id": video_id})
        HISTORY.parent.mkdir(exist_ok=True)
        HISTORY.write_text(json.dumps(history, ensure_ascii=False, indent=2))
    print("Listo:", out)


if __name__ == "__main__":
    main()

"""Locución gratuita con edge-tts (voces neuronales de Microsoft)."""
import asyncio
import subprocess
from pathlib import Path

import edge_tts

from config import VOICE, VOICE_RATE


async def _tts(text: str, path: str):
    await edge_tts.Communicate(text, VOICE, rate=VOICE_RATE).save(path)


def duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


def synth(scenes, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    for i, s in enumerate(scenes):
        path = str(outdir / f"scene_{i:02d}.mp3")
        asyncio.run(_tts(s["narration"], path))
        s["audio"] = path
        s["duration"] = duration(path) + 0.4  # pequeña pausa entre escenas

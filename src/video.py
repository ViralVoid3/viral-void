"""Montaje del vídeo con ffmpeg (clip de fondo + locución + subtítulos)."""
import subprocess
from pathlib import Path

from config import H, W


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr[-2000:])


def build_scene(scene: dict, clip, out: str):
    dur = scene["duration"]
    chunks = scene["chunks"]
    if clip:
        inputs = ["-stream_loop", "-1", "-i", clip]
    else:  # fondo liso si no hay clip de archivo
        inputs = ["-f", "lavfi", "-i", f"color=c=0x0f172a:s={W}x{H}:r=30"]
    for png, _, _ in chunks:
        inputs += ["-loop", "1", "-framerate", "30", "-i", png]
    inputs += ["-i", scene["audio"]]
    audio_idx = 1 + len(chunks)

    f = (f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
         f"crop={W}:{H},setsar=1,fps=30,format=yuv420p[v0]")
    for i, (_, s, e) in enumerate(chunks, 1):
        f += f";[v{i-1}][{i}:v]overlay=0:0:enable='between(t,{s:.2f},{e:.2f})'[v{i}]"

    run([
        "ffmpeg", "-y", *inputs, "-filter_complex", f,
        "-map", f"[v{len(chunks)}]", "-map", f"{audio_idx}:a",
        "-af", "apad", "-t", f"{dur:.2f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "44100", "-ac", "2", out,
    ])


def render(scenes, clips, workdir: Path, final: Path):
    workdir.mkdir(parents=True, exist_ok=True)
    parts = []
    for i, (s, clip) in enumerate(zip(scenes, clips)):
        out = str(workdir / f"scene_{i:02d}.mp4")
        build_scene(s, clip, out)
        parts.append(out)
    lst = workdir / "list.txt"
    lst.write_text("".join(f"file '{Path(p).resolve()}'\n" for p in parts))
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-c", "copy", "-movflags", "+faststart", str(final)])

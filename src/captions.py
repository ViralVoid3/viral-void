"""Fuentes y subtítulos (PNG transparentes superpuestos con ffmpeg)."""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config import H, W

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def font(size: int):
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _caption_png(text: str, path: Path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(56)
    lines = textwrap.wrap(text, width=42)[:3]
    line_h = 72
    box_h = line_h * len(lines) + 30
    y0 = H - box_h - 70
    d.rounded_rectangle((120, y0, W - 120, y0 + box_h), radius=24, fill=(0, 0, 0, 170))
    for i, line in enumerate(lines):
        w = d.textlength(line, font=f)
        d.text(((W - w) / 2, y0 + 15 + i * line_h), line, font=f, fill="white")
    img.save(path)


def render_chunks(scene: dict, outdir: Path, idx: int, words_per_chunk: int = 9):
    """Divide la narración en trozos y reparte el tiempo según su longitud."""
    outdir.mkdir(parents=True, exist_ok=True)
    words = scene["narration"].split()
    chunks = [" ".join(words[i:i + words_per_chunk]) for i in range(0, len(words), words_per_chunk)]
    total = max(len(words), 1)
    t = 0.0
    scene["chunks"] = []
    for j, text in enumerate(chunks):
        span = scene["duration"] * len(text.split()) / total
        png = outdir / f"cap_{idx:02d}_{j:02d}.png"
        _caption_png(text, png)
        scene["chunks"].append((str(png), t, t + span))
        t += span

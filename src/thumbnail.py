"""Miniatura 1280x720 con Pillow: foto oscurecida + texto grande."""
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw

from captions import font


def make(text: str, photo, out: Path):
    W, H = 1280, 720
    if photo and Path(photo).exists():
        img = Image.open(photo).convert("RGB")
        scale = max(W / img.width, H / img.height)
        img = img.resize((int(img.width * scale), int(img.height * scale)))
        left, top = (img.width - W) // 2, (img.height - H) // 2
        img = img.crop((left, top, left + W, top + H))
    else:
        img = Image.new("RGB", (W, H))
        d = ImageDraw.Draw(img)
        for y in range(H):  # degradado azul oscuro -> violeta
            k = y / H
            d.line([(0, y), (W, y)], fill=(int(15 + 70 * k), int(23 + 20 * k), int(60 + 90 * k)))

    shade = Image.new("RGBA", (W, H), (0, 0, 0, 110))
    img = Image.alpha_composite(img.convert("RGBA"), shade)
    d = ImageDraw.Draw(img)

    text = text.upper()
    size = 190
    while size > 70:
        f = font(size)
        lines = textwrap.wrap(text, width=max(8, int(1100 / (size * 0.62))))
        if len(lines) <= 3 and all(d.textlength(l, font=f) <= W - 120 for l in lines):
            break
        size -= 10
    line_h = int(size * 1.15)
    y = (H - line_h * len(lines)) // 2
    d.rectangle((0, 0, 28, H), fill=(255, 214, 10, 255))  # barra de acento
    for line in lines:
        w = d.textlength(line, font=f)
        d.text(((W - w) / 2, y), line, font=f, fill=(255, 214, 10),
               stroke_width=8, stroke_fill="black")
        y += line_h
    img.convert("RGB").save(out, quality=92)

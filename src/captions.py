
"""Fuentes y subtítulos adaptables para vídeos verticales de Viral Void."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from config import H, W

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

# Configuración visual
FONT_SIZE = 58
MIN_FONT_SIZE = 38
SIDE_MARGIN = int(W * 0.09)
MAX_TEXT_WIDTH = W - (SIDE_MARGIN * 2)
BOX_PADDING_X = 30
BOX_PADDING_Y = 22
LINE_SPACING = 14

# Posición vertical: distancia desde el borde inferior
BOTTOM_MARGIN = int(H * 0.17)


def font(size: int):
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def split_lines(text: str, draw, f, max_width: int):
    """Divide el texto midiendo el ancho real de cada línea."""
    words = text.split()
    lines = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip()

        if draw.textlength(candidate, font=f) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def fit_caption(text: str, draw):
    """Busca un tamaño de letra que permita mostrar el texto en 2 líneas."""
    for size in range(FONT_SIZE, MIN_FONT_SIZE - 1, -2):
        f = font(size)
        lines = split_lines(text, draw, f, MAX_TEXT_WIDTH - BOX_PADDING_X * 2)

        if len(lines) <= 2:
            return f, lines

    # Si el texto es excepcionalmente largo, permite más líneas
    f = font(MIN_FONT_SIZE)
    lines = split_lines(text, draw, f, MAX_TEXT_WIDTH - BOX_PADDING_X * 2)
    return f, lines


def _caption_png(text: str, path: Path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    f, lines = fit_caption(text, d)

    line_heights = [
        d.textbbox((0, 0), line, font=f)[3] -
        d.textbbox((0, 0), line, font=f)[1]
        for line in lines
    ]

    box_h = sum(line_heights) + LINE_SPACING * (len(lines) - 1)
    box_h += BOX_PADDING_Y * 2

    x0 = SIDE_MARGIN
    x1 = W - SIDE_MARGIN
    y0 = H - BOTTOM_MARGIN - box_h
    y1 = y0 + box_h

    d.rounded_rectangle(
        (x0, y0, x1, y1),
        radius=24,
        fill=(0, 0, 0, 185)
    )

    current_y = y0 + BOX_PADDING_Y

    for line, line_height in zip(lines, line_heights):
        text_width = d.textlength(line, font=f)
        x = (W - text_width) / 2

        d.text(
            (x, current_y),
            line,
            font=f,
            fill="white",
            stroke_width=1,
            stroke_fill=(0, 0, 0, 255)
        )

        current_y += line_height + LINE_SPACING

    img.save(path)


def render_chunks(scene: dict, outdir: Path, idx: int, words_per_chunk: int = 7):
    """Divide la narración en trozos y reparte el tiempo según su longitud."""
    outdir.mkdir(parents=True, exist_ok=True)

    words = scene["narration"].split()

    chunks = [
        " ".join(words[i:i + words_per_chunk])
        for i in range(0, len(words), words_per_chunk)
    ]

    total = max(len(words), 1)
    t = 0.0
    scene["chunks"] = []

    for j, text in enumerate(chunks):
        span = scene["duration"] * len(text.split()) / total

        png = outdir / f"cap_{idx:02d}_{j:02d}.png"
        _caption_png(text, png)

        scene["chunks"].append((str(png), t, t + span))
        t += span

#!/usr/bin/env python3

from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image


ROOT = Path(__file__).resolve().parent.parent
SVG = ROOT / "res" / "savoldesk.svg"
ICO_SIZES = [
    (16, 16),
    (20, 20),
    (24, 24),
    (32, 32),
    (40, 40),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]


def render_png(size: int) -> Image.Image:
    inner_size = max(1, round(size * 0.84))
    data = cairosvg.svg2png(
        url=str(SVG),
        output_width=inner_size,
        output_height=inner_size,
    )
    glyph = Image.open(BytesIO(data)).convert("RGBA")
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - inner_size) // 2, (size - inner_size) // 2)
    canvas.alpha_composite(glyph, offset)
    return canvas


def save_ico(path: Path, source: Image.Image) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    source.save(path, format="ICO", sizes=ICO_SIZES, bitmap_format="png")


def main() -> None:
    master = render_png(256)

    png_outputs = {
        ROOT / "res" / "32x32.png": 32,
        ROOT / "res" / "64x64.png": 64,
        ROOT / "res" / "128x128.png": 128,
        ROOT / "res" / "128x128@2x.png": 256,
        ROOT / "res" / "icon.png": 512,
    }
    for path, size in png_outputs.items():
        render_png(size).save(path, format="PNG")

    save_ico(ROOT / "res" / "icon.ico", master)
    save_ico(ROOT / "res" / "tray-icon.ico", master)
    save_ico(
        ROOT / "flutter" / "windows" / "runner" / "resources" / "app_icon.ico",
        master,
    )
    save_ico(ROOT / "flutter" / "assets" / "icon.ico", master)


if __name__ == "__main__":
    main()

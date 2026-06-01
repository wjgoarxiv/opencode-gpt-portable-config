#!/usr/bin/env python3

import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
OUT_PATH = ROOT / "cover.png"

W, H = 2560, 1280
CORNER_RADIUS = 80

BASE = (8, 12, 24, 255)
BLOBS = [
    (24, 94, 130, 210, 700, 600, 720, 500, 120),
    (56, 180, 205, 150, 1900, 210, 620, 390, 105),
    (20, 38, 92, 185, 1280, 1150, 930, 360, 95),
    (82, 120, 255, 105, 1400, 640, 520, 350, 85),
]
TITLE_GLOWS = [
    ((60, 220, 235, 58), 18),
    ((115, 190, 255, 88), 9),
    ((170, 230, 255, 115), 4),
]
TITLE_COLOR = (246, 250, 255, 248)
SUBTITLE_COLOR = (158, 190, 218, 216)


def make_blob(size, color_rgba, cx, cy, rx, ry):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color_rgba)
    return layer


def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def load_fonts():
    try:
        return (
            font("/System/Library/Fonts/Menlo.ttc", 220, index=1),
            font("/System/Library/Fonts/Menlo.ttc", 70, index=0),
        )
    except OSError:
        fallback = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
        return font(fallback, 220), font(fallback, 70)


def text_layer(text, x, y, selected_font, color):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((x, y), text, font=selected_font, fill=color)
    return layer


def centered_position(draw, text, selected_font):
    bbox = draw.textbbox((0, 0), text, font=selected_font)
    return bbox, (W - (bbox[2] - bbox[0])) // 2 - bbox[0]


def main():
    canvas = Image.new("RGBA", (W, H), BASE)

    for r, g, b, a, cx, cy, rx, ry, blur in BLOBS:
        blob = make_blob((W, H), (r, g, b, a), cx, cy, rx, ry)
        canvas = Image.alpha_composite(canvas, blob.filter(ImageFilter.GaussianBlur(radius=blur)))

    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=8))

    rng = np.random.default_rng(42)
    noise = rng.integers(0, 255, (H, W), dtype=np.uint8)
    grain_alpha = (noise * 0.20).astype(np.uint8)
    grain_layer = np.stack([noise, noise, noise, grain_alpha], axis=-1).astype(np.uint8)
    canvas = Image.alpha_composite(canvas, Image.fromarray(grain_layer, "RGBA"))

    title_font, subtitle_font = load_fonts()
    title_text = "opencode-config"
    subtitle_text = "Portable GPT routing for OpenCode agents."

    probe = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(probe)
    title_bbox, title_x = centered_position(draw, title_text, title_font)
    subtitle_bbox, subtitle_x = centered_position(draw, subtitle_text, subtitle_font)

    title_h = title_bbox[3] - title_bbox[1]
    subtitle_h = subtitle_bbox[3] - subtitle_bbox[1]
    gap = 48
    block_top = (H - (title_h + gap + subtitle_h)) // 2 - 30
    title_y = block_top - title_bbox[1]
    subtitle_y = title_y + title_h + gap - subtitle_bbox[1]

    for glow_color, blur_radius in TITLE_GLOWS:
        glow = text_layer(title_text, title_x, title_y, title_font, glow_color)
        canvas = Image.alpha_composite(canvas, glow.filter(ImageFilter.GaussianBlur(radius=blur_radius)))

    canvas = Image.alpha_composite(canvas, text_layer(title_text, title_x, title_y, title_font, TITLE_COLOR))
    canvas = Image.alpha_composite(
        canvas,
        text_layer(subtitle_text, subtitle_x, subtitle_y, subtitle_font, SUBTITLE_COLOR),
    )

    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (W - 1, H - 1)], radius=CORNER_RADIUS, fill=255)
    canvas.putalpha(mask)
    canvas = canvas.filter(ImageFilter.GaussianBlur(radius=1))
    canvas.save(OUT_PATH, "PNG", dpi=(400, 400))

    size_mb = os.path.getsize(OUT_PATH) / 1024 / 1024
    print(f"Saved: {OUT_PATH}")
    print(f"Size: {canvas.size}")
    print(f"Mode: {canvas.mode}")
    print(f"File: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()

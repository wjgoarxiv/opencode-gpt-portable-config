#!/usr/bin/env python3
"""Cover image — pretty terminal style. All JetBrains Mono Nerd Font."""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

DPI = 600
WIDTH = 5400
HEIGHT = 1800
RADIUS = 100
OUTPUT = os.path.join(os.path.dirname(__file__), "cover.png")

BG = (18, 20, 28)
WHITE = (235, 237, 245)

F_XBOLD = os.path.expanduser("~/Library/Fonts/JetBrainsMonoNLNerdFont-ExtraBold.ttf")
F_BOLD = os.path.expanduser("~/Library/Fonts/JetBrainsMonoNLNerdFont-Bold.ttf")
F_REG = os.path.expanduser("~/Library/Fonts/JetBrainsMonoNLNerdFont-Regular.ttf")
F_LIGHT = os.path.expanduser("~/Library/Fonts/JetBrainsMonoNLNerdFont-Light.ttf")


def center(draw, text, font, w):
    bb = draw.textbbox((0, 0), text, font=font)
    return (w - bb[2] + bb[0]) // 2


def main():
    # === 1. Black canvas ===
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 255))

    # === 2. Inner rounded rect with dark bg ===
    inner = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    inner_draw = ImageDraw.Draw(inner)
    pad = 40
    inner_draw.rounded_rectangle(
        [pad, pad, WIDTH - pad, HEIGHT - pad],
        radius=RADIUS, fill=BG
    )
    canvas = Image.alpha_composite(canvas, inner)

    # === 3. Constellation star field ===
    rng = np.random.default_rng(77)
    stars_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    stars_draw = ImageDraw.Draw(stars_layer)

    # Generate star positions
    n_stars = 180
    sx = rng.integers(pad + 60, WIDTH - pad - 60, size=n_stars)
    sy = rng.integers(pad + 60, HEIGHT - pad - 60, size=n_stars)
    s_bright = rng.integers(15, 55, size=n_stars)
    s_size = rng.choice([1, 1, 1, 2, 2, 3], size=n_stars)

    for i in range(n_stars):
        a = int(s_bright[i])
        r = int(s_size[i])
        x, y = int(sx[i]), int(sy[i])
        if r == 1:
            stars_draw.point((x, y), fill=(200, 210, 240, a))
        else:
            stars_draw.ellipse([x - r, y - r, x + r, y + r],
                               fill=(200, 210, 240, a))

    # Constellation lines — connect nearby stars
    for i in range(n_stars):
        for j in range(i + 1, n_stars):
            dx = float(sx[i] - sx[j])
            dy = float(sy[i] - sy[j])
            dist = math.sqrt(dx * dx + dy * dy)
            if 120 < dist < 350:
                # Only draw some connections
                if rng.random() < 0.12:
                    a = max(4, int(12 * (1.0 - dist / 350)))
                    stars_draw.line(
                        [(int(sx[i]), int(sy[i])), (int(sx[j]), int(sy[j]))],
                        fill=(140, 160, 200, a), width=1)

    canvas = Image.alpha_composite(canvas, stars_layer)

    # === 3b. Subtle horizontal CRT scanlines ===
    scan_arr = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
    for y in range(pad, HEIGHT - pad):
        if y % 4 == 0:
            scan_arr[y, pad:WIDTH - pad, :] = [0, 0, 0, 18]
    scan = Image.fromarray(scan_arr, "RGBA")
    canvas = Image.alpha_composite(canvas, scan)

    # === 4. Multi-color ambient glow (aurora-style) ===
    gcx, gcy = WIDTH // 2, int(HEIGHT * 0.36)

    # Broad diffuse base
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    grx, gry = int(WIDTH * 0.38), int(HEIGHT * 0.50)
    ImageDraw.Draw(glow).ellipse(
        [gcx - grx, gcy - gry, gcx + grx, gcy + gry],
        fill=(30, 45, 75, 255))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=250))
    canvas = Image.alpha_composite(canvas, glow)

    # Left — purple/magenta
    glow_l = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    lx = int(WIDTH * 0.25)
    ImageDraw.Draw(glow_l).ellipse(
        [lx - 600, gcy - 350, lx + 600, gcy + 350],
        fill=(90, 30, 130, 140))
    glow_l = glow_l.filter(ImageFilter.GaussianBlur(radius=250))
    canvas = Image.alpha_composite(canvas, glow_l)

    # Right — teal/cyan
    glow_r = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    rx = int(WIDTH * 0.75)
    ImageDraw.Draw(glow_r).ellipse(
        [rx - 600, gcy - 350, rx + 600, gcy + 350],
        fill=(20, 90, 110, 140))
    glow_r = glow_r.filter(ImageFilter.GaussianBlur(radius=250))
    canvas = Image.alpha_composite(canvas, glow_r)

    # Center bright core
    glow2 = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    grx2, gry2 = int(WIDTH * 0.16), int(HEIGHT * 0.28)
    ImageDraw.Draw(glow2).ellipse(
        [gcx - grx2, gcy - gry2, gcx + grx2, gcy + gry2],
        fill=(65, 75, 110, 255))
    glow2 = glow2.filter(ImageFilter.GaussianBlur(radius=160))
    canvas = Image.alpha_composite(canvas, glow2)

    # Bottom warm accent (under badges)
    glow_b = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    by_glow = int(HEIGHT * 0.78)
    ImageDraw.Draw(glow_b).ellipse(
        [gcx - 1200, by_glow - 200, gcx + 1200, by_glow + 200],
        fill=(40, 55, 80, 120))
    glow_b = glow_b.filter(ImageFilter.GaussianBlur(radius=180))
    canvas = Image.alpha_composite(canvas, glow_b)

    # === 5. Title text — "OpenCode" ===
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.truetype(F_XBOLD, 280)
    title = "OpenCode"
    tx = center(draw, title, title_font, WIDTH)
    ty = int(HEIGHT * 0.10)

    # Text glow
    tglow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ImageDraw.Draw(tglow).text((tx, ty), title, fill=(200, 205, 220, 80), font=title_font)
    tglow = tglow.filter(ImageFilter.GaussianBlur(radius=30))
    canvas = Image.alpha_composite(canvas, tglow)

    # Sharp text
    tl = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ImageDraw.Draw(tl).text((tx, ty), title, fill=WHITE, font=title_font)
    canvas = Image.alpha_composite(canvas, tl)

    # === 6. Subtitle — "Portable Config" ===
    sub_font = ImageFont.truetype(F_BOLD, 220)
    sub = "Portable Config"
    draw = ImageDraw.Draw(canvas)
    sx = center(draw, sub, sub_font, WIDTH)
    sy = ty + 320

    # Subtitle glow
    sglow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ImageDraw.Draw(sglow).text((sx, sy), sub, fill=(180, 185, 200, 50), font=sub_font)
    sglow = sglow.filter(ImageFilter.GaussianBlur(radius=25))
    canvas = Image.alpha_composite(canvas, sglow)

    sl = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ImageDraw.Draw(sl).text((sx, sy), sub, fill=WHITE, font=sub_font)
    canvas = Image.alpha_composite(canvas, sl)

    # === 7. Rainbow gradient underline ===
    line_y = sy + 270
    colors = [
        (80, 250, 160),   # green
        (100, 220, 255),  # cyan
        (140, 160, 255),  # blue
        (180, 120, 255),  # purple
        (255, 100, 180),  # pink
        (255, 160, 80),   # orange
    ]

    line_len = 1400
    line_sx = (WIDTH - line_len) // 2
    line_img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    line_draw = ImageDraw.Draw(line_img)

    for x in range(line_len):
        prog = x / line_len
        seg = prog * (len(colors) - 1)
        idx = min(int(seg), len(colors) - 2)
        t = seg - idx
        c1, c2 = colors[idx], colors[idx + 1]
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)

        # Edge fade
        fade = 1.0
        if x < 100:
            fade = x / 100
        elif x > line_len - 100:
            fade = (line_len - x) / 100

        a = int(230 * fade)
        px = line_sx + x
        for dy in range(5):
            line_draw.point((px, line_y + dy), fill=(r, g, b, a))

    # Line glow
    lglow = line_img.filter(ImageFilter.GaussianBlur(radius=12))
    canvas = Image.alpha_composite(canvas, lglow)
    canvas = Image.alpha_composite(canvas, line_img)

    # === 8. Tagline ===
    tag_font = ImageFont.truetype(F_LIGHT, 56)
    tag = "GPT-5.4 for complex work, Codex for coding."
    draw = ImageDraw.Draw(canvas)
    tag_x = center(draw, tag, tag_font, WIDTH)
    tag_y = line_y + 55

    tag_l = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ImageDraw.Draw(tag_l).text((tag_x, tag_y), tag, fill=(170, 175, 190, 180), font=tag_font)
    canvas = Image.alpha_composite(canvas, tag_l)

    # === 9. Model badges — clean, no spec text ===
    badge_font_label = ImageFont.truetype(F_BOLD, 72)
    badge_font_model = ImageFont.truetype(F_REG, 80)

    badges = [
        ("\uf0e7 COMPLEX", "gpt-5.4", (80, 250, 160)),
        ("\uf121 CODING", "gpt-5.3-codex", (100, 220, 255)),
        ("\uf544 HELPER", "gpt-5.3-codex-spark", (170, 160, 255)),
    ]

    bw, bh = 1600, 230
    gap = 120
    total = len(badges) * bw + gap * (len(badges) - 1)
    bsx = (WIDTH - total) // 2
    by = int(HEIGHT * 0.72)

    badge_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge_layer)

    for i, (label, model, color) in enumerate(badges):
        bx = bsx + i * (bw + gap)

        # Subtle fill
        bd.rounded_rectangle([bx, by, bx + bw, by + bh], radius=16,
                             fill=(25, 28, 38, 140),
                             outline=(*color, 50), width=2)

        # Left accent bar
        bd.rounded_rectangle([bx + 10, by + 14, bx + 17, by + bh - 14],
                             radius=3, fill=(*color, 170))

        # Label
        bd.text((bx + 40, by + 20), label, fill=(*color, 240), font=badge_font_label)

        # Model name
        bd.text((bx + 40, by + 110), model, fill=(*WHITE, 225), font=badge_font_model)

    canvas = Image.alpha_composite(canvas, badge_layer)

    # === 10. Clip to rounded rect (outer is transparent) ===
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, WIDTH - 1, HEIGHT - 1], radius=RADIUS + 40, fill=255
    )
    bg_transparent = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    final = Image.composite(canvas, bg_transparent, mask)

    # === Save ===
    final.save(OUTPUT, "PNG", dpi=(DPI, DPI))
    mb = os.path.getsize(OUTPUT) / 1024 / 1024
    print(f"Saved: {OUTPUT}")
    print(f"{WIDTH}x{HEIGHT} @ {DPI} DPI  ({mb:.1f} MB)")


if __name__ == "__main__":
    main()

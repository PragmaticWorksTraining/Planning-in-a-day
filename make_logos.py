#!/usr/bin/env python3
"""Generate six Cordova division logos as PNG (96px + 512px)."""
import math, os
from PIL import Image, ImageDraw, ImageFont

S = 8                    # supersample factor
BASE = 96                # design grid
N = BASE * S             # working canvas
OUT = "logos"
FONT_BOLD = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"

DIVISIONS = [
    dict(slug="cordova-biosolutions",   initials="CBS", color="#1B6AC9", glyph="helix"),
    dict(slug="cordova-neurosciences",  initials="CNS", color="#2F6F3E", glyph="neuron"),
    dict(slug="cordova-cardio-labs",    initials="CCL", color="#C2334D", glyph="heart"),
    dict(slug="cordova-oncology",       initials="CO",  color="#6B3FA0", glyph="cell"),
    dict(slug="cordova-consumer-health",initials="CCH", color="#E0761B", glyph="leaf"),
    dict(slug="cordova-respiratory",    initials="CR",  color="#0E9488", glyph="lungs"),
]

W = (255, 255, 255, 255)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(rgb, f):
    return tuple(max(0, min(255, int(c * f))) for c in rgb)


def bezier(pts, steps=160):
    """De Casteljau for an arbitrary-order bezier."""
    out = []
    for i in range(steps + 1):
        t = i / steps
        p = list(pts)
        while len(p) > 1:
            p = [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
                 for a, b in zip(p, p[1:])]
        out.append(p[0])
    return out


def tile(color):
    """Rounded-square tile with a subtle vertical gradient."""
    rgb = hex2rgb(color)
    top, bot = shade(rgb, 1.10), shade(rgb, 0.88)
    grad = Image.new("RGB", (1, N))
    for y in range(N):
        t = y / (N - 1)
        grad.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    grad = grad.resize((N, N))
    mask = Image.new("L", (N, N), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, N - 1, N - 1], radius=int(0.215 * N), fill=255)
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    img.paste(grad, (0, 0), mask)
    return img


# ---------------------------------------------------------------- glyphs
# Glyph box: x 24..72, y 14..58 on the 96 grid (scaled by S).

def g(v):
    return v * S


def draw_helix(d, col):
    """Double helix: two strands over two full turns, with base-pair rungs."""
    y0, y1 = g(14), g(58)
    amp, midx = g(14.5), g(48)
    turns = 1.25
    lw = int(2.8 * S)
    strands = []
    for phase in (0, math.pi):
        pts = []
        for i in range(201):
            t = i / 200
            y = y0 + (y1 - y0) * t
            x = midx + amp * math.sin(turns * 2 * math.pi * t + phase)
            pts.append((x, y))
        strands.append(pts)
    # rungs first, so the strands read as passing in front of them
    for t in (0.10, 0.23, 0.36, 0.50, 0.64, 0.77, 0.90):
        y = y0 + (y1 - y0) * t
        off = amp * math.sin(turns * 2 * math.pi * t) * 0.78
        d.line([(midx - off, y), (midx + off, y)], fill=W, width=int(1.7 * S))
    for pts in strands:
        d.line(pts, fill=W, width=lw, joint="curve")


def draw_neuron(d, col):
    """Neuron: soma with dendrites on one side, axon and terminals on the other."""
    cx, cy, r = g(40), g(34), g(7.2)
    lw = int(2.7 * S)
    nr = g(2.2)
    # dendrites fan out to the left
    for ang, ln in ((168, 15.5), (205, 14.5), (135, 14.0), (250, 13.0)):
        a = math.radians(ang)
        x2, y2 = cx + math.cos(a) * g(ln), cy + math.sin(a) * g(ln)
        d.line([(cx, cy), (x2, y2)], fill=W, width=lw)
        d.ellipse([x2 - nr, y2 - nr, x2 + nr, y2 + nr], fill=W)
    # axon sweeps right, then branches into terminals
    axon = bezier([(cx + r * 0.6, cy + g(1)), (g(52), g(40)), (g(58), g(42)), (g(64), g(46))])
    d.line(axon, fill=W, width=lw, joint="curve")
    tip = axon[-1]
    for ex, ey in ((g(71), g(42)), (g(70), g(50)), (g(64), g(54))):
        d.line([tip, (ex, ey)], fill=W, width=int(2.2 * S))
        d.ellipse([ex - nr, ey - nr, ex + nr, ey + nr], fill=W)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=W)


def draw_heart(d, col):
    """Filled heart with an ECG trace knocked out of it."""
    cx, cy = g(48), g(34)
    sc = g(1.0)
    pts = []
    for i in range(241):
        t = i / 240 * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * sc * 1.32, cy + y * sc * 1.32))
    d.polygon(pts, fill=W)
    ecg = [(g(28), g(35)), (g(38), g(35)), (g(41.5), g(26)), (g(46), g(44)),
           (g(50), g(33)), (g(53), g(35)), (g(68), g(35))]
    d.line(ecg, fill=col, width=int(3.2 * S), joint="curve")


def draw_cell(d, col):
    """Membrane ring with nucleus and satellite bodies."""
    cx, cy, r = g(48), g(36), g(19)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=W, width=int(3.0 * S))
    nr = g(6.6)
    d.ellipse([cx - nr, cy - nr, cx + nr, cy + nr], fill=W)
    for ang, dist, sr in ((35, 12.2, 2.5), (160, 12.8, 2.1), (265, 12.0, 1.8)):
        a = math.radians(ang)
        x, y = cx + math.cos(a) * g(dist), cy + math.sin(a) * g(dist)
        d.ellipse([x - g(sr), y - g(sr), x + g(sr), y + g(sr)], fill=W)


def draw_leaf(d, col):
    """Two-arc leaf with midrib and side veins."""
    tip, base = (g(48), g(14)), (g(48), g(58))
    right = bezier([tip, (g(74), g(24)), (g(66), g(50)), base])
    left = bezier([base, (g(30), g(50)), (g(22), g(24)), tip])
    d.polygon(right + left, fill=W)
    d.line([(g(48), g(20)), (g(48), g(56))], fill=col, width=int(2.3 * S))
    for ty, dy in ((27, 5.5), (35, 6.5), (43, 5.5)):
        for sgn in (-1, 1):
            d.line([(g(48), g(ty + dy)), (g(48 + sgn * 9.5), g(ty))],
                   fill=col, width=int(1.9 * S))


def draw_lungs(d, col):
    """Trachea and bronchi above two lobes that widen downward."""
    lw = int(2.9 * S)
    d.line([(g(48), g(13)), (g(48), g(29))], fill=W, width=lw)
    d.line([(g(48), g(29)), (g(42), g(35))], fill=W, width=lw)
    d.line([(g(48), g(29)), (g(54), g(35))], fill=W, width=lw)
    for sgn in (-1, 1):
        x = lambda v: g(48 + sgn * v)
        outer = bezier([(x(5), g(33)), (x(20), g(37)), (x(22), g(52)), (x(14), g(58))])
        bottom = bezier([(x(14), g(58)), (x(8), g(59)), (x(5), g(55)), (x(5), g(50))])
        d.polygon(outer + bottom + [(x(5), g(33))], fill=W)


GLYPHS = dict(helix=draw_helix, neuron=draw_neuron, heart=draw_heart,
              cell=draw_cell, leaf=draw_leaf, lungs=draw_lungs)


def build(div):
    col = hex2rgb(div["color"])
    img = tile(div["color"])
    d = ImageDraw.Draw(img)
    GLYPHS[div["glyph"]](d, col + (255,))

    # initials, letterspaced, centred on the lower band
    txt = div["initials"]
    f = ImageFont.truetype(FONT_BOLD, int(17.5 * S))
    track = int(1.2 * S)
    widths = [d.textlength(c, font=f) for c in txt]
    total = sum(widths) + track * (len(txt) - 1)
    x = (N - total) / 2
    y = g(63.5)
    for c, w in zip(txt, widths):
        d.text((x, y), c, font=f, fill=W)
        x += w + track
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    for div in DIVISIONS:
        big = build(div)
        for size in (512, 96):
            out = big.resize((size, size), Image.LANCZOS)
            out.save(f"{OUT}/{div['slug']}{'' if size == 96 else '@512'}.png",
                     optimize=True)
        print(f"{div['slug']:28s} {div['initials']:4s} {div['color']}")

    # contact sheet for review
    sheet = Image.new("RGB", (96 * 6 + 7 * 12, 96 + 24), (245, 245, 247))
    for i, div in enumerate(DIVISIONS):
        sheet.paste(Image.open(f"{OUT}/{div['slug']}.png"), (12 + i * 108, 12),
                    Image.open(f"{OUT}/{div['slug']}.png"))
    sheet.save("contact_96.png")

    big = Image.new("RGB", (512 * 3 + 4 * 24, 512 * 2 + 3 * 24), (245, 245, 247))
    for i, div in enumerate(DIVISIONS):
        im = Image.open(f"{OUT}/{div['slug']}@512.png")
        big.paste(im, (24 + (i % 3) * 536, 24 + (i // 3) * 536), im)
    big.save("contact_512.png")


if __name__ == "__main__":
    main()

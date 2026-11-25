#!/usr/bin/env python3
"""THE MERIDIAN STANDARD — News Image 20261125, Akun 13.
One day (Tuesday 25 November 2026) drawn as a single 1024x1024 front
page: black ink and brick red on ivory. Two layout variants (A/B) are
rendered from the same locked story pool and duelled; the winner is
copied to entry.png. PIL is used locally to draw; the submitted
main.py is copy-only and needs nothing beyond the standard library.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
MX = 26

IVORY = (243, 238, 224)
IVORY_D = (236, 228, 205)
INK = (26, 24, 20)
MUTE = (96, 88, 74)
RED = (158, 44, 32)
RED_D = (122, 32, 24)
GOLD = (176, 141, 62)
SKY = (203, 213, 216)
SEA = (84, 110, 116)
SAND = (214, 199, 158)
GREEN = (88, 104, 62)
WHITE = (250, 248, 240)


def F(size, bold=False, disp=False, italic=False):
    if disp:
        name = "PlayfairDisplay-Black.ttf" if bold or True else "PlayfairDisplay.ttf"
        name = "PlayfairDisplay-Black.ttf"
    elif italic:
        name = "PlayfairDisplay-Italic.ttf"
    elif bold:
        name = "Archivo-Bold.ttf"
    else:
        name = "Archivo.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def T(d, xy, s, font, fill=INK, anchor=None):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- pool
# num, region tag, headline, deck, source, tag (REPORTED/CLAIMED/SCHEDULED), chip
CARDS = {
    1: ("1 · EUROPE — POLAND", "NATO sends early-warning jets to Poland",
        "NATO plans an AWACS deployment in Poland after Russian missiles "
        "landed in Poland during an attack on Ukraine; Chancellor Merz "
        "vows complete German support.", "wire reports", "REPORTED",
        "AWACS TO POLAND"),
    2: ("2 · MIDDLE EAST — STRAIT OF HORMUZ", "Iran says 3 tankers hit by mines",
        "The IRGC Navy claims three oil tankers were hit by naval mines "
        "in the Strait of Hormuz; shipping concerns rise on the claim.",
        "Iranian claim via wires", "CLAIMED", "3 TANKERS HIT — IRAN SAYS"),
    3: ("3 · MIDDLE EAST — IRAQ", "Baghdad orders Kurdish oilfields seized",
        "PM Ali al-Zaidi directs federal units to seize oilfields and "
        "crossings in Kurdish-run regions; President Barzani answers "
        "that Kurdistan will not submit to unconstitutional decisions.",
        "Starlit / wires", "REPORTED", "OILFIELDS ORDER"),
    6: ("6 · WORLD — UKRAINE", "700,000 Russian dead, new count finds",
        "New analysis finds more than 700,000 Russian soldiers killed "
        "in the nearly five-year war on Ukraine.", "RFE/RL", "REPORTED",
        "700,000+ KILLED"),
    4: ("4 · MIDDLE EAST — GAZA", "Drone strikes kill Hamas security chief",
        "Israeli drone strikes across Gaza killed 7 people: a senior "
        "Hamas security official, three policemen and three siblings, "
        "one a child.", "Al Jazeera", "REPORTED", "7 KILLED IN STRIKES"),
    5: ("5 · EUROPE — BRUSSELS", "EU unveils new Russia sanctions",
        "The European Union announced further restrictive measures "
        "against Russia amid the war in Ukraine — another turn of the "
        "sanctions screw on Tuesday.", "wire roundups", "REPORTED",
        "NEW EU SANCTIONS"),
    36: ("36 · WORLD — NVIDIA", "Nvidia's $1 trillion Monday",
         "Monday close: Nvidia shares +31.5%, nearly $1 trillion of "
         "market value clawed back as Huang returned as CEO, +$34bn "
         "in a day.", "Forbes via wires", "REPORTED", "+31.5% MONDAY CLOSE"),
    33: ("33 · WORLD — WASHINGTON", "PCE inflation report due today",
         "The US PCE inflation report is due Tuesday 25 November; "
         "markets watch for the Fed's next signal. No figure yet — "
         "none is printed here.", "scheduled", "SCHEDULED", "PCE DUE TODAY"),
    11: ("11 · EUROPE — MADRID", "Madrid rout PSV 5-1 in comeback",
         "Real Madrid overturned a deficit to beat PSV Eindhoven 5-1; "
         "a Bellingham stunner and an Mbappé brace.", "wire reports",
         "REPORTED", "MADRID 5-1 PSV"),
    13: ("13 · OCEANIA — AUSTRALIA", "12 coral species brought back",
         "Great Barrier Reef genetic analysis resurrects 12 Acropora "
         "coral species; reef diversity wider than known.",
         "science wires", "REPORTED", "12 SPECIES BACK"),
    10: ("10 · ASIA — CHINA", "Xiamen Airlines orders 50 Boeing jets",
         "Xiamen Airlines, a China Southern unit, agreed to acquire "
         "50 Boeing 737-8 jets.", "wire reports", "REPORTED",
         "50 JETS ORDERED"),
    37: ("37 · AMERICAS — USA", "Storms target Thanksgiving travel",
         "Inclement weather targeting both US shorelines poses a risk "
         "to Thanksgiving travel for millions.", "wire reports",
         "REPORTED", "STORMS BOTH COASTS"),
    26: ("26 · ASIA-PACIFIC — SOLOMONS", "Solomons eye Australia treaty switch",
         "Solomon Islands plans to replace its China defence treaty "
         "with an Australia treaty, according to reports from the "
         "Pacific.", "wire reports", "REPORTED", "TREATY SWITCH"),
}
LEADS = [1, 2, 3]
GRID = [6, 4, 5, 36, 33, 11, 13, 10, 37, 26]

BRIEFS = [
    (7, "First 5 Lynx KF41 IFVs enter Ukrainian service"),
    (8, "Colombia car bomb injures at least 23"),
    (9, "Gunmen hold dozens in a Cartagena supermarket"),
    (12, "England level T20 series, chasing 185"),
    (14, "Fiji declares disaster in El Niño dry spell"),
    (15, "Iran pharmacies run dry in medicine shortage"),
    (16, "Iran braces for winter gas shortages"),
    (17, "Britain sanctions the Houthis' top leaders"),
    (18, "Senegal AFCON title restored by CAS ruling"),
    (19, "Rebels pull back in DR Congo after clashes"),
    (20, "Nigerian emir suspended after allegation"),
    (21, "Sudan RSF commander defects"),
    (22, "Cameroon separatist in Norway court"),
    (23, "Punjab: BJP and Akali Dal reunite as allies"),
    (24, "Bangladesh opens Guangzhou investment office"),
    (25, "Indonesia's vice-president resigns"),
    (27, "North Korea touts China ties in Pyongyang"),
    (28, "Denmark court upholds ghetto evictions law"),
    (29, "Sarkozy headed for Libya-case trial"),
    (30, "Black Sea clash at the UN"),
    (31, "Shortwave school for Afghan girls"),
    (32, "Dimorphos casts its shadow on Didymos"),
    (34, "US targets 7 firms over chip diversion"),
    (35, "Moscow buys inflatable decoys from China"),
]

NUMBERS = [
    ("700,000+", "RUSSIAN DEAD — NEW COUNT"),
    ("3", "TANKERS HIT — IRAN SAYS"),
    ("7", "KILLED IN GAZA STRIKES"),
    ("50", "BOEING 737-8 JETS ORDERED"),
    ("5–1", "MADRID OVER PSV"),
    ("+31.5%", "NVIDIA — MONDAY CLOSE"),
    ("12", "CORAL SPECIES BACK"),
    ("23", "INJURED, COLOMBIA BOMB"),
]
REGIONS = [("EUROPE", 8), ("MIDDLE EAST", 6), ("WORLD", 6), ("AFRICA", 5),
           ("AMERICAS", 4), ("ASIA", 2), ("SOUTH ASIA", 2),
           ("ASIA-PACIFIC", 2), ("OCEANIA", 2)]
TIMELINE = [
    ("EARLY", "NATO AWACS plan for Poland reported"),
    ("MORNING", "Iran says 3 tankers mined at Hormuz"),
    ("MIDDAY", "Baghdad oilfield order reaches Kurdistan"),
    ("TODAY", "US PCE report due — no figure yet"),
    ("MON CLOSE", "Nvidia +31.5% — Monday close, Forbes"),
    ("TONIGHT", "Storms target Thanksgiving travel"),
]
DATECHECK = [
    "GTA VI launch hype — a game date, not today's news",
    "COP31 talks — earlier this month, not Tuesday",
    "Liverpool 4–0 — a weekend score, not 25 November",
    "Mercury stories filed 23 Nov — two days old, excluded",
    "Black Friday sales — Friday's story, not Tuesday's",
]


# ---------------------------------------------------------------- scenes
def _sky(d, x, y, w, h, top, bot):
    steps = 24
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.rectangle([x, y + h * i // steps, x + w, y + h * (i + 1) // steps + 1], fill=c)


def sc_awacs(d, x, y, w, h):
    _sky(d, x, y, w, h, (168, 186, 196), (226, 230, 220))
    cy = y + h * 0.52
    d.ellipse([x + w * 0.30, cy - h * 0.34, x + w * 0.70, cy + h * 0.30], outline=RED, width=3)
    d.ellipse([x + w * 0.40, cy - h * 0.20, x + w * 0.60, cy + h * 0.16], outline=RED_D, width=2)
    d.polygon([(x + w * 0.18, cy), (x + w * 0.62, cy - h * 0.06), (x + w * 0.80, cy),
               (x + w * 0.62, cy + h * 0.05)], fill=INK)
    d.polygon([(x + w * 0.20, cy - h * 0.02), (x + w * 0.10, cy - h * 0.20),
               (x + w * 0.24, cy - h * 0.16)], fill=RED)
    d.rectangle([x + w * 0.44, cy - h * 0.16, x + w * 0.54, cy - h * 0.08], fill=INK)


def sc_tanker(d, x, y, w, h):
    _sky(d, x, y, w, h, (150, 168, 175), (120, 142, 148))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    for sx in (0.16, 0.52, 0.84):
        bx, by = x + w * sx, y + h * 0.60
        d.polygon([(bx - 16, by), (bx + 16, by), (bx + 9, by + 9), (bx - 9, by + 9)], fill=INK)
        d.rectangle([bx - 11, by - 7, bx + 11, by], fill=RED_D)
    mx, my = x + w * 0.34, y + h * 0.80
    d.polygon([(mx, my - 12), (mx + 4, my - 2), (mx + 11, my + 2), (mx + 4, my + 5),
               (mx, my + 12), (mx - 4, my + 5), (mx - 11, my + 2), (mx - 4, my - 2)], fill=INK)
    d.line([x, y + h * 0.97, x + w, y + h * 0.97], fill=IVORY, width=1)


def sc_oilfield(d, x, y, w, h):
    _sky(d, x, y, w, h, (226, 205, 160), (240, 228, 190))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=SAND)
    for fx in (0.24, 0.62):
        bx, by = x + w * fx, y + h * 0.78
        d.line([bx - 20, by, bx, by - h * 0.52], fill=INK, width=3)
        d.line([bx + 20, by, bx, by - h * 0.52], fill=INK, width=3)
        d.line([bx - 15, by - h * 0.18, bx + 15, by - h * 0.18], fill=INK, width=2)
        d.line([bx, by - h * 0.52, bx + 26, by - h * 0.40], fill=INK, width=3)
        d.polygon([(bx + 26, by - h * 0.40), (bx + 34, by - h * 0.30), (bx + 22, by - h * 0.30)], fill=RED)
    d.ellipse([x + w * 0.86, y + h * 0.10, x + w * 0.97, y + h * 0.28], fill=GOLD)


def sc_field(d, x, y, w, h):
    _sky(d, x, y, w, h, (74, 72, 84), (128, 116, 104))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(96, 86, 66))
    import random
    rng = random.Random(6)
    for _ in range(46):
        cx = x + rng.uniform(0.03, 0.97) * w
        cy = y + rng.uniform(0.64, 0.94) * h
        s = rng.uniform(3, 6)
        d.line([cx - s, cy, cx + s, cy], fill=IVORY, width=2)
        d.line([cx, cy - s, cx, cy + s], fill=IVORY, width=2)


def sc_drone(d, x, y, w, h):
    _sky(d, x, y, w, h, (96, 92, 96), (168, 148, 128))
    base = y + h * 0.86
    for i, bh in enumerate((0.30, 0.44, 0.24, 0.52, 0.36, 0.28)):
        bx = x + w * (0.04 + i * 0.155)
        d.rectangle([bx, base - h * bh, bx + w * 0.11, base], fill=(52, 48, 48))
        d.rectangle([bx + 3, base - h * bh + 4, bx + 7, base - h * bh + 8], fill=GOLD)
    d.rectangle([x, base, x + w, y + h], fill=(70, 60, 52))
    qx, qy = x + w * 0.60, y + h * 0.20
    d.rectangle([qx - 16, qy - 3, qx + 16, qy + 3], fill=INK)
    for dx in (-20, 20):
        d.ellipse([qx + dx - 6, qy - 8, qx + dx + 6, qy - 3], outline=INK, width=2)
    d.line([qx, qy + 3, qx, qy + 12], fill=INK, width=2)


def sc_dome(d, x, y, w, h):
    _sky(d, x, y, w, h, (172, 184, 196), (224, 226, 214))
    cx, base = x + w / 2, y + h * 0.88
    d.pieslice([cx - w * 0.30, base - h * 0.72, cx + w * 0.30, base + h * 0.20], 180, 360, fill=(196, 198, 200), outline=INK, width=2)
    d.rectangle([cx - w * 0.34, base, cx + w * 0.34, base + 3], fill=INK)
    for i in range(6):
        a = 3.14159 * (0.12 + i * 0.15)
        sx = cx + w * 0.21 * __import__("math").cos(a)
        sy = base - h * 0.40 * __import__("math").sin(a)
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=GOLD, outline=INK)


def sc_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 40, 36))
    cw, ch = w * 0.34, h * 0.52
    cx, cy = x + (w - cw) / 2, y + (h - ch) / 2
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=(52, 84, 62), outline=GOLD, width=2)
    d.rectangle([cx + 8, cy + 8, cx + cw - 8, cy + ch - 8], outline=(120, 200, 140), width=1)
    for i in range(5):
        px = cx + cw * (0.12 + i * 0.19)
        d.line([px, cy - 8, px, cy], fill=GOLD, width=3)
        d.line([px, cy + ch, px, cy + ch + 8], fill=GOLD, width=3)
    for i in range(3):
        py = cy + ch * (0.25 + i * 0.25)
        d.line([cx - 8, py, cx, py], fill=GOLD, width=3)
        d.line([cx + cw, py, cx + cw + 8, py], fill=GOLD, width=3)
    pts = [(0.1, 0.78), (0.3, 0.62), (0.5, 0.68), (0.7, 0.38), (0.9, 0.16)]
    d.line([(x + px * w, y + py * h) for px, py in pts], fill=(240, 120, 90), width=3)


def sc_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 233, 216))
    for i in range(4):
        gy = y + h * (0.2 + i * 0.2)
        d.line([x + 8, gy, x + w - 8, gy], fill=(200, 192, 168), width=1)
    pts = [(0.08, 0.62), (0.28, 0.55), (0.46, 0.60), (0.64, 0.47), (0.80, 0.52)]
    d.line([(x + px * w, y + py * h) for px, py in pts], fill=INK, width=3)
    ex, ey = x + w * 0.92, y + h * 0.40
    d.ellipse([ex - 13, ey - 13, ex + 13, ey + 13], outline=RED, width=3)
    T(d, (ex, ey - 1), "?", F(17, True), RED, anchor="mm")
    d.line([x + w * 0.80, y + h * 0.52, ex - 8, ey + 6], fill=RED, width=2)


def sc_stadium(d, x, y, w, h):
    _sky(d, x, y, w, h, (44, 52, 74), (84, 96, 110))
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=GREEN)
    d.ellipse([x + w * 0.30, y + h * 0.62, x + w * 0.70, y + h * 0.94], outline=IVORY, width=2)
    d.line([x + w * 0.5, y + h * 0.60, x + w * 0.5, y + h * 0.96], fill=IVORY, width=1)
    for fx in (0.10, 0.90):
        px = x + w * fx
        d.line([px, y + h * 0.52, px, y + h * 0.16], fill=INK, width=3)
        d.ellipse([px - 9, y + h * 0.08, px + 9, y + h * 0.17], fill=(250, 240, 200))
    T(d, (x + w * 0.5, y + h * 0.30), "5–1", F(26, True), IVORY, anchor="mm")


def sc_coral(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 96, 110))
    d.rectangle([x, y + h * 0.80, x + w, y + h], fill=(196, 182, 140))

    def branch(bx, by, ang, ln, wd, col, depth):
        import math
        ex, ey = bx + ln * math.cos(ang), by - ln * math.sin(ang)
        d.line([bx, by, ex, ey], fill=col, width=max(1, wd))
        if depth <= 0 or ln < 5:
            d.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=(240, 170, 150))
            return
        branch(ex, ey, ang + 0.42, ln * 0.72, wd - 1, col, depth - 1)
        branch(ex, ey, ang - 0.38, ln * 0.72, wd - 1, col, depth - 1)

    branch(x + w * 0.30, y + h * 0.86, 1.35, h * 0.30, 5, (226, 120, 96), 4)
    branch(x + w * 0.62, y + h * 0.88, 1.65, h * 0.36, 5, (240, 160, 110), 4)
    branch(x + w * 0.84, y + h * 0.84, 1.45, h * 0.24, 4, (226, 120, 96), 3)


def sc_jet(d, x, y, w, h):
    _sky(d, x, y, w, h, (158, 182, 200), (228, 232, 224))
    cy = y + h * 0.46
    d.polygon([(x + w * 0.10, cy), (x + w * 0.78, cy - h * 0.05), (x + w * 0.92, cy),
               (x + w * 0.78, cy + h * 0.07), (x + w * 0.16, cy + h * 0.05)], fill=(238, 238, 240), outline=INK)
    d.polygon([(x + w * 0.14, cy - h * 0.02), (x + w * 0.06, cy - h * 0.20),
               (x + w * 0.20, cy - h * 0.17)], fill=RED)
    d.polygon([(x + w * 0.44, cy + h * 0.03), (x + w * 0.34, cy + h * 0.20),
               (x + w * 0.52, cy + h * 0.16)], fill=(200, 204, 208), outline=INK)
    for i in range(9):
        wx = x + w * (0.30 + i * 0.055)
        d.ellipse([wx, cy - h * 0.015, wx + 5, cy + h * 0.02], fill=(90, 120, 150))


def sc_storm(d, x, y, w, h):
    _sky(d, x, y, w, h, (86, 94, 104), (140, 148, 150))
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(70, 92, 100))
    for i in range(3):
        wy = y + h * (0.74 + i * 0.09)
        d.arc([x + w * (0.06 + i * 0.22), wy, x + w * (0.30 + i * 0.22), wy + h * 0.08], 180, 360, fill=IVORY, width=2)
    cx, cy = x + w * 0.72, y + h * 0.30
    for r in (26, 17, 9):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=IVORY, width=3)
    for lx in (0.16, 0.34):
        px = x + w * lx
        d.line([px, y + h * 0.06, px - 5, y + h * 0.20], fill=GOLD, width=2)
        d.line([px - 5, y + h * 0.20, px + 3, y + h * 0.20], fill=GOLD, width=2)
        d.line([px + 3, y + h * 0.20, px - 3, y + h * 0.34], fill=GOLD, width=2)


def sc_islands(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(86, 128, 138))
    d.ellipse([x + w * 0.10, y + h * 0.30, x + w * 0.46, y + h * 0.62], fill=SAND, outline=INK)
    d.ellipse([x + w * 0.56, y + h * 0.44, x + w * 0.90, y + h * 0.72], fill=SAND, outline=INK)
    for px, py in ((0.26, 0.40), (0.72, 0.54)):
        bx, by = x + w * px, y + h * py
        d.line([bx, by + 8, bx, by - 8], fill=(70, 84, 50), width=3)
        d.polygon([(bx, by - 8), (bx - 9, by - 2), (bx + 9, by - 2)], fill=(70, 84, 50))
    sx, sy = x + w * 0.50, y + h * 0.20
    d.rectangle([sx - 16, sy - 10, sx + 16, sy + 10], fill=(240, 234, 214), outline=INK)
    d.line([sx - 16, sy - 10, sx + 16, sy + 10], fill=RED, width=1)
    d.line([sx + 16, sy - 10, sx - 16, sy + 10], fill=RED, width=1)


SCENES = {1: sc_awacs, 2: sc_tanker, 3: sc_oilfield, 6: sc_field, 4: sc_drone,
          5: sc_dome, 36: sc_chip, 33: sc_chart, 11: sc_stadium, 13: sc_coral,
          10: sc_jet, 37: sc_storm, 26: sc_islands}

# dotted world map: rows of a coarse grid, '#' = land
MAP = [
    "..........####..........######..####........................................",
    "......##########......##############......##..####..........................",
    ".....###########.....################....##########.........................",
    "......########......#################...############..##....................",
    ".......######........###############.....##########.........................",
    "........####..........#############........######......#....................",
    ".........##............###########..........####............................",
    ".........##.............########............###..........##.................",
    "........###..............######.............##..........####................",
    "........####..............####.........................######...............",
    "........#####..............###........................########..............",
    ".........####...............#........................#########..............",
    ".........###........................................##########.......##.....",
    ".........##..........................................########.......####....",
    "..........#...........................................######.........##.....",
    ".......................................................####...................",
    ".......................................................##..........##.........",
    "..................................................................####........",
    "...................................................................##.........",
]


def draw_map(d, x, y, w, h, pins):
    rows, cols = len(MAP), len(MAP[0])
    cw, ch = w / cols, h / rows
    for r, row in enumerate(MAP):
        for c, cell in enumerate(row):
            if cell == "#":
                cx, cy = x + c * cw, y + r * ch
                d.ellipse([cx, cy, cx + cw * 0.72, cy + ch * 0.72], fill=(150, 138, 108))
    for num, fx, fy in pins:
        cx, cy = x + fx * w, y + fy * h
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED, outline=IVORY, width=2)
        T(d, (cx, cy - 1), str(num), F(9, True), IVORY, anchor="mm")


PINS = [(1, 0.485, 0.16), (2, 0.565, 0.30), (3, 0.575, 0.27), (6, 0.53, 0.15),
        (4, 0.565, 0.26), (5, 0.475, 0.14), (36, 0.075, 0.22), (33, 0.10, 0.24),
        (11, 0.465, 0.20), (13, 0.885, 0.78), (10, 0.76, 0.28), (37, 0.11, 0.20),
        (26, 0.90, 0.62)]


# ---------------------------------------------------------------- cards
def draw_card(d, num, x, y, w, h, lead=False):
    region, head, deck, source, tag, chip = CARDS[num]
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=1)
    band = RED_D if lead else INK
    d.rectangle([x, y, x + w, y + 15], fill=band)
    T(d, (x + 5, y + 3), region, F(8, True), IVORY)
    T(d, (x + w - 5, y + 3), tag, F(8, True), (240, 205, 150), anchor="ra")
    scene_h = int(h * (0.40 if lead else 0.34))
    SCENES[num](d, x + 3, y + 18, w - 6, scene_h)
    ty = y + 22 + scene_h
    hf = F(19, disp=True) if lead else F(12, True)
    for line in wrap(d, head, hf, w - 12):
        if ty + 14 > y + h - 18:
            break
        T(d, (x + 6, ty), line, hf, INK)
        ty += (23 if lead else 15)
    df = F(11) if lead else F(9)
    for line in wrap(d, deck, df, w - 12):
        if ty + (13 if lead else 11) > y + h - 18:
            break
        T(d, (x + 6, ty), line, df, (52, 48, 42))
        ty += (14 if lead else 11)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=IVORY_D, outline=INK)
    T(d, (x + 5, y + h - 12), chip, F(8, True), RED_D)
    T(d, (x + w - 5, y + h - 12), source, F(7), MUTE, anchor="ra")


def number_strip(d, y):
    cw = (W - 2 * MX) / 8
    d.line([MX, y, W - MX, y], fill=INK, width=2)
    for i, (big, lab) in enumerate(NUMBERS):
        x = MX + i * cw
        if i:
            d.line([x, y + 4, x, y + 32], fill=(196, 182, 140), width=1)
        T(d, (x + cw / 2, y + 3), big, F(19, True), INK, anchor="ma")
        for j, line in enumerate(wrap(d, lab, F(7, True), cw - 6)):
            T(d, (x + cw / 2, y + 24 + j * 8), line, F(7, True), MUTE, anchor="ma")
    d.line([MX, y + 42, W - MX, y + 42], fill=INK, width=1)
    return y + 48


def region_strip(d, y):
    x = MX
    T(d, (x, y + 2), "REGIONS:", F(10, True), INK)
    x += d.textlength("REGIONS: ", font=F(10, True))
    fills = [(196, 74, 54), (158, 44, 32), (122, 32, 24), (176, 141, 62),
             (84, 110, 116), (88, 104, 62), (104, 88, 120), (70, 120, 130),
             (150, 120, 70)]
    for i, (name, n) in enumerate(REGIONS):
        label = f"{name} {n}"
        tw = d.textlength(label, font=F(9, True)) + 12
        d.rectangle([x, y, x + tw, y + 16], fill=fills[i % len(fills)])
        T(d, (x + 6, y + 3), label, F(9, True), IVORY)
        x += tw + 5
    return y + 22


def briefs_block(d, y, h):
    d.rectangle([MX, y, W - MX, y + 17], fill=INK)
    T(d, (MX + 6, y + 3), "ALSO ON THE PAGE — 24 MORE DATED STORIES, NUMBERED AS REPORTED",
      F(10, True), IVORY)
    cols = 4
    cw = (W - 2 * MX) / cols
    rows = (len(BRIEFS) + cols - 1) // cols
    rh = (h - 22) / rows
    for idx, (num, text) in enumerate(BRIEFS):
        cx = MX + (idx // rows) * cw
        cy = y + 21 + (idx % rows) * rh
        s = f"{num}. {text}"
        T(d, (cx + 2, cy), s, F(9), INK)
    return y + h


def bottom_row(d, y, h, order):
    widths = {"map": 0.44, "time": 0.28, "date": 0.28}
    x = MX
    total = W - 2 * MX
    for i, kind in enumerate(order):
        w = total * widths[kind] - (6 if i < 2 else 0)
        if kind == "map":
            d.rectangle([x, y, x + w, y + 15], fill=INK)
            T(d, (x + 5, y + 3), "THE DAY ON THE MAP — PINS ARE CARD NUMBERS", F(9, True), IVORY)
            draw_map(d, x + 4, y + 19, w - 8, h - 36, PINS)
            T(d, (x + 5, y + h - 13),
              "1 POLAND · 2 HORMUZ · 3 IRAQ · 6 UKRAINE · 4 GAZA · 5 BRUSSELS · 36 NVIDIA",
              F(7, True), MUTE)
            T(d, (x + 5, y + h - 5),
              "33 WASHINGTON · 11 MADRID · 13 GBR REEF · 10 CHINA · 37 US COASTS · 26 SOLOMONS",
              F(7, True), MUTE)
        elif kind == "time":
            d.rectangle([x, y, x + w, y + 15], fill=RED_D)
            T(d, (x + 5, y + 3), "THE DAY IN SIX HOURS", F(9, True), IVORY)
            ty = y + 21
            for when, what in TIMELINE:
                T(d, (x + 5, ty), when, F(8, True), RED_D)
                for line in wrap(d, what, F(9), w - 62):
                    T(d, (x + 60, ty), line, F(9), INK)
                    ty += 11
                ty += 4
        else:
            d.rectangle([x, y, x + w, y + 15], fill=INK)
            T(d, (x + 5, y + 3), "DATE CHECK — NOT TODAY", F(9, True), IVORY)
            ty = y + 21
            for item in DATECHECK:
                T(d, (x + 5, ty), "×", F(10, True), RED)
                for line in wrap(d, item, F(9), w - 22):
                    T(d, (x + 17, ty), line, F(9), INK)
                    ty += 11
                ty += 3
        x += w + 6
    return y + h


def footer(d):
    T(d, (MX, 1002),
      "Sources: RFE/RL · Al Jazeera · DW · Starlit Daily · Forbes via wires · wire roundups. Claims are labelled as claims.",
      F(8), MUTE)
    T(d, (W - MX, 1002), "Original drawings, drawn for this page.", F(8), MUTE, anchor="ra")
    T(d, (W / 2, 1013), "THE MERIDIAN STANDARD · TUESDAY 25 NOVEMBER 2026 · ONE DAY, ONE PAGE",
      F(8, True), INK, anchor="ma")


# ---------------------------------------------------------------- layouts
def layout_a():
    img = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(img)
    T(d, (MX, 8), "ONE DAY · 37 DATED STORIES · 13 FULL-SCENE CARDS · 9 REGIONS",
      F(11, True), INK)
    T(d, (W - MX, 8), "EVERY FIGURE FROM TODAY'S WIRES", F(11, True), RED_D, anchor="ra")
    d.line([MX, 30, W - MX, 30], fill=INK, width=2)
    T(d, (W / 2, 38), "THE MERIDIAN STANDARD", F(52, disp=True), INK, anchor="ma")
    T(d, (W / 2, 94), "TUESDAY 25 NOVEMBER 2026", F(15, True), RED, anchor="ma")
    d.line([MX, 114, W - MX, 114], fill=INK, width=2)
    y = number_strip(d, 120)
    y = region_strip(d, y + 2)
    y += 6
    draw_card(d, 1, MX, y, W - 2 * MX, 140, lead=True)
    y += 146
    hw = (W - 2 * MX - 8) / 2
    draw_card(d, 2, MX, y, hw, 140, lead=True)
    draw_card(d, 3, MX + hw + 8, y, hw, 140, lead=True)
    y += 146
    cw = (W - 2 * MX - 4 * 6) / 5
    for r in range(2):
        for c in range(5):
            num = GRID[r * 5 + c]
            draw_card(d, num, MX + c * (cw + 6), y, cw, 142)
        y += 148
    y = briefs_block(d, y + 2, 88)
    bottom_row(d, y + 6, 990 - (y + 6), ["map", "time", "date"])
    footer(d)
    return img


def layout_b():
    img = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(img)
    T(d, (MX, 8), "ONE DAY — ONE PAGE — EVERY STORY DATED AND SOURCED", F(11, True), INK)
    T(d, (W - MX, 8), "37 STORIES — 9 REGIONS", F(11, True), RED_D, anchor="ra")
    d.rectangle([MX, 28, W - MX, 98], fill=INK)
    T(d, (MX + 16, 40), "THE MERIDIAN STANDARD", F(38, disp=True), IVORY)
    T(d, (MX + 18, 82), "BLACK INK & BRICK RED — THE DAY, MEASURED", F(9, True), (216, 190, 150))
    d.rectangle([W - MX - 218, 36, W - MX - 8, 90], fill=RED_D)
    T(d, (W - MX - 113, 42), "TUESDAY", F(17, True), IVORY, anchor="ma")
    T(d, (W - MX - 113, 64), "25 NOVEMBER 2026", F(17, True), IVORY, anchor="ma")
    y = number_strip(d, 106)
    y = region_strip(d, y + 2)
    y += 6
    lw = (W - 2 * MX - 2 * 8) / 3
    for i, num in enumerate(LEADS):
        draw_card(d, num, MX + i * (lw + 8), y, lw, 216, lead=True)
    y += 222
    cw = (W - 2 * MX - 4 * 6) / 5
    for r in range(2):
        for c in range(5):
            num = GRID[r * 5 + c]
            draw_card(d, num, MX + c * (cw + 6), y, cw, 160)
        y += 166
    y = briefs_block(d, y + 2, 100)
    bottom_row(d, y + 6, 990 - (y + 6), ["date", "map", "time"])
    footer(d)
    return img


def render(variant):
    return layout_a() if variant == "A" else layout_b()


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, f"entry_{variant.lower()}.png")
    render(variant).save(out, optimize=True)
    print("saved", out)

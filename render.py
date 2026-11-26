"""Render entry.png (1024x1024) for news-image-20261126.

World news of Thursday 26 November 2026, six verified stories only.
Fonts: DejaVu Sans Condensed / Serif Condensed (bundled with the 22 Nov entry).
Run: python3 render.py  ->  entry.png
"""
import math
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = '/home/hatch/workspace/makefun/news-image-20261122-review/dejavu-fonts-ttf-2.37/ttf/'
B  = FONT_DIR + 'DejaVuSansCondensed-Bold.ttf'
R  = FONT_DIR + 'DejaVuSansCondensed.ttf'
SB = FONT_DIR + 'DejaVuSerifCondensed-Bold.ttf'
OUT = 'entry.png'

W = H = 1024
NAVY = '#14284B'
PAPER = '#F6F3EC'
RED = '#C0392B'
GOLD = '#F2C14E'

im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)
F = lambda p, s: ImageFont.truetype(p, s)


def wrap(text, font, width):
    """Greedy word wrap to the given pixel width."""
    lines, cur = [], ''
    for word in text.split(' '):
        trial = (cur + ' ' + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wtext(x, y, w, text, font, fill='#111', sp=2):
    """Draw centred wrapped lines; return y below the last line."""
    for line in wrap(text, font, w):
        tw = d.textlength(line, font=font)
        d.text((x + (w - tw) / 2, y), line, font=font, fill=fill)
        y += font.size + sp
    return y


def ctext(x, y, w, text, font, fill='#111', sp=3):
    """Draw centred lines; return y below the last line."""
    for line in text.split('\n'):
        tw = d.textlength(line, font=font)
        d.text((x + (w - tw) / 2, y), line, font=font, fill=fill)
        y += font.size + sp
    return y


def ltext(x, y, w, text, font, fill='#333', sp=4):
    """Draw left-aligned wrapped text; return y below the last line."""
    for line in wrap(text, font, w):
        d.text((x, y), line, font=font, fill=fill)
        y += font.size + sp
    return y


def card(x, y, w, h, col):
    d.rectangle([x, y, x + w, y + h], fill='white', outline='#BBBBBB')
    d.rectangle([x, y, x + w, y + 7], fill=col)


def tag(x, y, w, t, col):
    f = F(B, 14)
    tw = d.textlength(t, font=f) + 22
    d.rounded_rectangle([x + (w - tw) / 2, y, x + (w + tw) / 2, y + 22], 11, fill=col)
    ctext(x, y + 3, w, t, f, 'white')


# ---------- icons ----------
def ic_ship(x, y, w, h):
    """Container ship on the sea."""
    d.rectangle([x, y, x + w, y + h], fill='#BFD9E8')
    d.rectangle([x, y, x + w, y + int(h * 0.62)], fill='#8FB8D4')
    # stacked containers
    cols = ['#C0392B', '#2E5D9F', '#D4A017', '#1A9C8F', '#7D3C98']
    cw_, ch_ = 52, 30
    base = y + h - 78
    for row in range(2):
        for i in range(6):
            cx = x + 28 + i * (cw_ + 6)
            cy = base - row * (ch_ + 4)
            d.rectangle([cx, cy, cx + cw_, cy + ch_], fill=cols[(i + row) % 5],
                        outline='#333333', width=2)
    # hull
    d.polygon([(x + 10, base + 4), (x + w - 10, base + 4), (x + w - 60, base + 34),
               (x + 60, base + 34)], fill='#14284B')
    d.rectangle([x + w - 120, base - 26, x + w - 60, base + 4], fill='#F6F3EC',
                outline='#333333', width=2)
    # waves
    for i in range(5):
        wx = x + 20 + i * 80
        d.arc([wx, base + 44, wx + 60, base + 62], 0, 180, fill='#2E5D9F', width=3)


def ic_refinery(x, y, w, h):
    """Oil refinery towers with a flame."""
    d.rectangle([x, y, x + w, y + h], fill='#E8D9B8')
    d.rectangle([x, y, x + w, y + int(h * 0.55)], fill='#F2C14E')
    # flare stack with flame
    sx = x + w - 52
    d.rectangle([sx, y + 26, sx + 14, y + h - 8], fill='#5A5A5A')
    d.polygon([(sx - 8, y + 28), (sx + 7, y + 2), (sx + 22, y + 28)], fill='#E67E22')
    d.polygon([(sx - 2, y + 28), (sx + 7, y + 12), (sx + 16, y + 28)], fill='#F2C14E')
    # distillation towers
    for i, tw_ in enumerate((34, 46, 30)):
        tx = x + 18 + i * 52
        d.rectangle([tx, y + h - 96, tx + tw_, y + h - 8], fill='#8C9BA5',
                    outline='#333333', width=2)
        d.rectangle([tx - 3, y + h - 108, tx + tw_ + 3, y + h - 96], fill='#5A5A5A')
    # pipes
    d.line([x + 18, y + h - 40, x + w - 60, y + h - 40], fill='#333333', width=4)
    # oil barrel
    bx, by = x + 22, y + h - 70
    d.ellipse([bx, by, bx + 26, by + 10], fill='#C0392B')
    d.rectangle([bx, by + 5, bx + 26, by + 34], fill='#C0392B')
    d.ellipse([bx, by + 28, bx + 26, by + 38], fill='#8E2A20')


def ic_market(x, y, w, h):
    """Supermarket storefront with striped awning."""
    d.rectangle([x, y, x + w, y + h], fill='#DDE7EA')
    # awning
    for i in range(6):
        ax = x + 8 + i * (w - 16) // 6
        col = '#C0392B' if i % 2 == 0 else '#F6F3EC'
        d.polygon([(ax, y + 8), (ax + (w - 16) // 6, y + 8),
                   (ax + (w - 16) // 6, y + 34), (ax, y + 34)], fill=col)
    d.rectangle([x + 8, y + 34, x + w - 8, y + 40], fill='#14284B')
    # shop front
    d.rectangle([x + 14, y + 40, x + w - 14, y + h - 10], fill='#F6F3EC',
                outline='#333333', width=2)
    d.rectangle([x + 26, y + 52, x + w - 26, y + h - 34], fill='#9CC3E4',
                outline='#333333', width=2)
    # shelves inside the window
    for j in range(2):
        sy = y + 66 + j * 22
        d.line([x + 30, sy, x + w - 30, sy], fill='#333333', width=2)
        for k in range(4):
            px = x + 36 + k * 40
            d.rectangle([px, sy - 12, px + 14, sy], fill=['#C0392B', '#2E5D9F',
                        '#D4A017', '#1A9C8F'][(j + k) % 4])
    # door
    d.rectangle([x + w // 2 - 22, y + h - 34, x + w // 2 + 22, y + h - 10],
                fill='#2E5D9F')
    # people (small figures) outside
    for i in range(3):
        px = x + 30 + i * 46
        base = y + h - 8
        d.ellipse([px - 7, base - 26, px + 7, base - 12], fill='#1D3557')
        d.rectangle([px - 8, base - 12, px + 8, base], fill='#1D3557')


def ic_scales(x, y, w, h):
    """Scales of justice."""
    d.rectangle([x, y, x + w, y + h], fill='#E7E7E7')
    cx, cy = x + w / 2, y + h / 2
    d.rectangle([cx - 4, y + 22, cx + 4, y + h - 22], fill='#14284B')
    d.line([cx - 78, y + 30, cx + 78, y + 30], fill='#14284B', width=5)
    d.polygon([(cx - 10, y + 22), (cx + 10, y + 22), (cx, y + 10)], fill='#C0392B')
    for sgn in (-1, 1):
        px = cx + sgn * 78
        d.line([px, y + 30, px, y + 62], fill='#14284B', width=3)
        d.arc([px - 34, y + 52, px + 34, y + 96], 0, 180, fill='#C0392B', width=5)
        d.line([px - 34, y + 72, px + 34, y + 72], fill='#C0392B', width=3)
    d.rectangle([cx - 46, y + h - 22, cx + 46, y + h - 14], fill='#14284B')


def ic_rocket(x, y, w, h):
    """Rocket climbing past stars."""
    d.rectangle([x, y, x + w, y + h], fill='#14284B')
    for sx, sy, r in [(x + 20, y + 16, 3), (x + w - 24, y + 30, 2),
                      (x + 34, y + 60, 2), (x + w - 40, y + 90, 3),
                      (x + w // 2, y + 12, 2)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill='white')
    cx, cy = x + w / 2, y + h / 2 - 6
    d.polygon([(cx, cy - 52), (cx + 20, cy - 8), (cx + 20, cy + 26),
               (cx - 20, cy + 26), (cx - 20, cy - 8)], fill='#F6F3EC',
              outline='#C0392B', width=2)
    d.polygon([(cx, cy - 52), (cx + 12, cy - 26), (cx - 12, cy - 26)], fill='#C0392B')
    d.ellipse([cx - 8, cy + 8, cx + 8, cy + 24], fill='#2E5D9F',
              outline='#C0392B', width=2)
    d.polygon([(cx - 20, cy + 26), (cx - 38, cy + 48), (cx - 20, cy + 40)],
              fill='#C0392B')
    d.polygon([(cx + 20, cy + 26), (cx + 38, cy + 48), (cx + 20, cy + 40)],
              fill='#C0392B')
    d.polygon([(cx - 10, cy + 26), (cx, cy + 58), (cx + 10, cy + 26)],
              fill='#F2C14E')
    d.polygon([(cx - 5, cy + 26), (cx, cy + 44), (cx + 5, cy + 26)],
              fill='#E67E22')


def ic_turkey(x, y, w, h):
    """Thanksgiving turkey with fanned tail."""
    d.rectangle([x, y, x + w, y + h], fill='#E8C99B')
    cx, cy = x + w / 2, y + h - 26
    # tail feathers fan upward from the body
    for i, ang in enumerate((-55, -33, -11, 11, 33, 55)):
        a = math.radians(ang)
        tx = cx + 66 * math.sin(a)
        ty = cy - 6 - 66 * math.cos(a)
        d.line([cx, cy - 6, tx, ty], fill='#8C5A2B', width=9)
        d.ellipse([tx - 13, ty - 13, tx + 13, ty + 13],
                  fill=['#C0392B', '#D4A017', '#7D3C98', '#2E5D9F',
                        '#1A9C8F', '#E67E22'][i])
    # body
    d.ellipse([cx - 34, cy - 40, cx + 34, cy + 14], fill='#8C5A2B')
    d.ellipse([cx - 26, cy - 30, cx + 26, cy + 6], fill='#A9713F')
    # wing
    d.ellipse([cx - 22, cy - 26, cx + 6, cy + 2], fill='#6B4423')
    # neck + head
    d.ellipse([cx + 8, cy - 62, cx + 34, cy - 28], fill='#8C5A2B')
    d.ellipse([cx + 16, cy - 76, cx + 40, cy - 52], fill='#8C5A2B')
    d.polygon([(cx + 38, cy - 64), (cx + 52, cy - 58), (cx + 38, cy - 56)],
              fill='#F2C14E')
    d.ellipse([cx + 28, cy - 68, cx + 32, cy - 64], fill='black')
    d.ellipse([cx + 22, cy - 52, cx + 30, cy - 38], fill='#C0392B')


# ---------- masthead ----------
d.rectangle([24, 18, 1000, 148], fill=NAVY)
ctext(24, 26, 976, 'THE WORLD IN ONE DAY', F(SB, 64), 'white')
ctext(24, 102, 976, 'THURSDAY, 26 NOVEMBER 2026', F(B, 30), GOLD)

# ---------- layout ----------
M = 24
G = 12
top = 162
cw = (W - 2 * M - 3 * G) // 4          # 235
r1h = 420
lw = 2 * cw + G                        # 482 lead width
top2 = top + r1h + G                   # 594
r2h = H - top2 - 70                    # 360
cw3 = (W - 2 * M - 2 * G) // 3         # 317

# ---------- lead story: US tariffs ----------
lx = M
card(lx, top, lw, r1h, '#2E5D9F')
d.text((lx + 16, top + 18), 'LEAD STORY', font=F(B, 15), fill=RED)
ic_ship(lx + 16, top + 44, lw - 32, 130)
yy = ctext(lx, top + 188, lw, 'US PLANS NEW TARIFFS\nON 14 TRADE PARTNERS',
           F(SB, 36), '#111111', 4)
yy = ltext(lx + 20, yy + 8, lw - 40,
           "Trump administration cites 'structural overcapacity' in a new "
           "Section 301 move. China faces the highest rate; Taiwan up to 15%. "
           "S&P 500 futures fall 2.1%, Nasdaq 100 down 3.1%.",
           F(R, 18), '#333333', 5)
tag(lx, top + r1h - 36, lw, 'US · TRADE', '#2E5D9F')


def small_card(x, col, tg, hd, sub, icon, hsz=21):
    card(x, top, cw, r1h, col)
    ih = int(r1h * 0.32)
    icon(x + 10, top + 16, cw - 20, ih)
    yy = wtext(x, top + 24 + ih, cw, hd, F(B, hsz), '#111111', 2)
    ltext(x + 10, yy + 8, cw - 20, sub, F(R, 14), '#333333', 3)
    tag(x, top + r1h - 32, cw, tg, col)


small_card(M + (2) * (cw + G), '#8E2A20', 'MIDDLE EAST · ENERGY',
           'HOUTHIS CLAIM STRIKE ON SAUDI REFINERY',
           "Yemen's Houthis claim an attack on Ras Tanura, Saudi Arabia's "
           "largest refinery (550,000 barrels a day). The coalition says 4 "
           "drones were shot down; no casualties reported. Brent +3.5% "
           "to $94.61; WTI +2% to $83.68.",
           ic_refinery)

small_card(M + (3) * (cw + G), '#1A7A4C', 'COLOMBIA',
           'CARTAGENA HOSTAGES ALL FREED',
           "After a ~17-hour standoff at an Exito supermarket, security "
           "forces storm in and free every remaining hostage. One gunman is "
           "killed; 10 people were freed earlier.",
           ic_market)


def row2_card(x, w, col, tg, hd, sub, icon, hsz=21):
    card(x, top2, w, r2h, col)
    ih = int(r2h * 0.36)
    icon(x + 10, top2 + 16, w - 20, ih)
    yy = wtext(x, top2 + 24 + ih, w, hd, F(B, hsz), '#111111', 2)
    ltext(x + 10, yy + 8, w - 20, sub, F(R, 14), '#333333', 3)
    tag(x, top2 + r2h - 32, w, tg, col)


row2_card(M, cw3, '#7D3C98', 'SOUTH AFRICA',
          "COURT RULES RAMAPHOSA IMPEACHMENT REPORT UNLAWFUL",
          "A South African court rules the impeachment report against "
          "President Ramaphosa unlawful.",
          ic_scales)

row2_card(M + cw3 + G, cw3, '#2E5D9F', 'SPACE',
          "FIRST FOREIGN ASTRONAUT ABOARD CHINA'S SPACE STATION",
          "Pakistan's Muhammad Zeeshan Ali arrives aboard Shenzhou-24 — the "
          "first foreign astronaut to visit Tiangong.",
          ic_rocket)

row2_card(M + 2 * (cw3 + G), cw3 + 1, '#C0392B', 'USA · THANKSGIVING',
          'THANKSGIVING TURKEY PARDON',
          "At the White House ceremony, a turkey named Feathers runs off "
          "into the bushes instead of taking the stage. VP JD Vance serves "
          "troops Thanksgiving meals in Ohio.",
          ic_turkey)

# ---------- footer ----------
fy = H - 52
d.line([M, fy, W - M, fy], fill='#333333', width=2)
ctext(0, fy + 8, W,
      'Data as of 26 Nov 2026 · Sources: Reuters, Al Jazeera, AFP, NDTV, AP',
      F(R, 14), '#333333')
ctext(0, fy + 28, W, '"~" = approximately, as reported', F(R, 12), '#666666')

im.save(OUT)
print('saved', OUT, im.size)

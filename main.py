#!/usr/bin/env python3
"""SockMatch 3000 - catalogue photograph of an impossible gadget.

Draws, from scratch with Pillow only, a studio product shot of a small
white machine that automatically pairs socks. Two metal clamp arms hold
up a freshly matched pair of red-striped socks; the screen reads
MATCH / PAIR FOUND. Exactly one accessory: a single lonely blue-striped
sock lying on the floor to the right.

Output: /output/entry.png (1024x1024 PNG, <= 1 MiB). No network.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

# ---------------------------------------------------------------- palette
BG_TOP = (250, 248, 245)
BG_MID = (242, 239, 234)
FLOOR_TOP = (232, 228, 222)
FLOOR_BOT = (214, 209, 202)
BODY = (252, 252, 250)
BODY_EDGE = (190, 188, 182)
DARK = (38, 40, 44)
SCREEN = (16, 22, 20)
GREEN = (46, 204, 113)
GREEN_DK = (30, 160, 84)
METAL = (196, 198, 202)
METAL_DK = (140, 142, 148)
METAL_LT = (232, 233, 235)
RED = (214, 48, 49)
BLUE = (52, 120, 198)
INK = (52, 54, 58)
SOFT = (120, 116, 108)


def load_font(bold=False, size=24):
    """DejaVu ships with most Linux images; fall back to the bitmap font."""
    cands = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in cands:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default(size)


def vgrad(size, top, bottom):
    """Vertical gradient image."""
    w, h = size
    img = Image.new("RGB", (1, h))
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return img.resize((w, h))


def soft_shadow(base, box, blur, alpha):
    """Blurred dark ellipse shadow pasted onto base."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=(60, 55, 48, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


def rrect(d, box, radius, **kw):
    d.rounded_rectangle(box, radius=radius, **kw)


# ------------------------------------------------------------------- socks
def make_sock(stripe, scale=1.0, flip=False):
    """Return an RGBA image of one hanging sock.

    Local layout (before scaling): cuff across the top, leg hanging down,
    foot bending to the right at the ankle, toe cap in the stripe colour.
    """
    sw, sh = int(120 * scale), int(300 * scale)
    sock = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d = ImageDraw.Draw(sock)
    s = scale

    # Silhouette mask: leg + foot.
    mask = Image.new("L", (sw, sh), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([18 * s, 6 * s, 102 * s, 185 * s], radius=26 * s, fill=255)
    md.rounded_rectangle([18 * s, 150 * s, 118 * s, 235 * s], radius=34 * s, fill=255)
    md.ellipse([86 * s, 168 * s, 122 * s, 252 * s], fill=255)
    md.rectangle([18 * s, 150 * s, 105 * s, 235 * s], fill=255)

    # White body, then stripes clipped by the silhouette.
    body = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body)
    bd.rectangle([0, 0, sw, sh], fill=(250, 250, 248, 255))
    for y0 in (52, 96, 140, 196):
        bd.rectangle([0, y0 * s, sw, (y0 + 20) * s], fill=stripe + (255,))
    # Cuff band at the top, striped.
    bd.rectangle([0, 6 * s, sw, 40 * s], fill=(244, 244, 242, 255))
    for x0 in (26, 58, 90):
        bd.rectangle([x0 * s, 6 * s, (x0 + 12) * s, 40 * s], fill=stripe + (255,))
    # Toe cap.
    bd.ellipse([84 * s, 176 * s, 122 * s, 250 * s], fill=stripe + (255,))
    # Heel patch.
    bd.ellipse([6 * s, 168 * s, 40 * s, 214 * s], fill=(238, 238, 236, 255))
    # Soft shading on the right edge of the leg.
    bd.rectangle([96 * s, 40 * s, 104 * s, 185 * s], fill=(0, 0, 0, 22))
    body.putalpha(Image.composite(body.split()[3], Image.new("L", (sw, sh), 0), mask))
    sock.alpha_composite(body)

    # Cuff ribbing lines.
    d.line([(22 * s, 14 * s), (22 * s, 34 * s)], fill=(0, 0, 0, 40), width=max(2, int(2 * s)))
    d.line([(98 * s, 14 * s), (98 * s, 34 * s)], fill=(0, 0, 0, 40), width=max(2, int(2 * s)))
    if flip:
        sock = sock.transpose(Image.FLIP_LEFT_RIGHT)
    return sock


def make_flat_sock(stripe):
    """One sock lying flat on the floor (the lonely accessory)."""
    sw, sh = 210, 110
    sock = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    mask = Image.new("L", (sw, sh), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([6, 18, 150, 92], radius=30, fill=255)
    md.ellipse([118, 14, 204, 96], fill=255)
    md.rectangle([118, 18, 168, 92], fill=255)
    body = Image.new("RGBA", (sw, sh), (250, 250, 248, 255))
    bd = ImageDraw.Draw(body)
    for x0 in (34, 74, 114):
        bd.rectangle([x0, 18, x0 + 16, 92], fill=stripe + (255,))
    bd.ellipse([152, 24, 200, 86], fill=stripe + (255,))
    bd.rectangle([6, 18, 30, 92], fill=(244, 244, 242, 255))
    bd.rectangle([178, 18, 184, 92], fill=(0, 0, 0, 18))
    body.putalpha(Image.composite(body.split()[3], Image.new("L", (sw, sh), 0), mask))
    sock.alpha_composite(body)
    return sock


# ------------------------------------------------------------------- arms
def draw_arm(d, base_xy, tip_xy, width=20):
    """A brushed-metal clamp arm: dark under-stroke, light core, joint."""
    d.line([base_xy, tip_xy], fill=METAL_DK, width=width + 6)
    d.line([base_xy, tip_xy], fill=METAL, width=width)
    d.line([base_xy, tip_xy], fill=METAL_LT, width=max(4, width // 3))
    d.ellipse([base_xy[0] - 14, base_xy[1] - 14, base_xy[0] + 14, base_xy[1] + 14],
              fill=METAL_DK, outline=METAL_LT, width=3)
    d.ellipse([base_xy[0] - 6, base_xy[1] - 6, base_xy[0] + 6, base_xy[1] + 6],
              fill=DARK)


def draw_clamp(d, tip_xy):
    """Small dark gripper jaw at the end of an arm."""
    x, y = tip_xy
    d.rounded_rectangle([x - 26, y - 12, x + 26, y + 12], radius=6,
                        fill=DARK, outline=(0, 0, 0), width=2)
    d.rectangle([x - 26, y - 12, x - 12, y + 12], fill=(70, 72, 76))
    d.rectangle([x + 12, y - 12, x + 26, y + 12], fill=(70, 72, 76))


# ------------------------------------------------------------------- main
def main():
    img = Image.new("RGBA", (W, H))
    bg = vgrad((W, H), BG_TOP, BG_MID).convert("RGBA")
    img.paste(bg, (0, 0))

    # Soft key-light bloom, upper left.
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-260, -320, 620, 420], fill=(255, 255, 255, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img.alpha_composite(glow)

    # Floor: horizon at y=772, gentle gradient below it.
    floor = vgrad((W, H - 772), FLOOR_TOP, FLOOR_BOT).convert("RGBA")
    img.paste(floor, (0, 772))
    d = ImageDraw.Draw(img)
    d.line([(0, 772), (W, 772)], fill=(198, 192, 184), width=2)

    # Contact shadows (device + lonely sock), before the objects.
    soft_shadow(img, (210, 726, 780, 786), 16, 90)
    soft_shadow(img, (742, 812, 986, 852), 10, 70)

    # (Arms and socks are drawn after the body, below, so they hang in
    # front of the machine and the whole sock - foot included - reads.)

    # ---------------------------------------------------------- the body
    body_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(body_layer)
    rrect(bd, (252, 372, 728, 730), 40, fill=BODY + (255,),
          outline=BODY_EDGE, width=3)
    # Side shading + top highlight so the white shell reads as moulded plastic.
    rrect(bd, (688, 380, 726, 722), 30, fill=(0, 0, 0, 18))
    rrect(bd, (254, 374, 292, 722), 30, fill=(255, 255, 255, 90))
    rrect(bd, (268, 380, 712, 404), 18, fill=(255, 255, 255, 140))
    # Plinth / base.
    rrect(bd, (238, 722, 742, 752), 16, fill=(74, 76, 80, 255))
    rrect(bd, (238, 722, 742, 736), 16, fill=(104, 106, 110, 255))
    img.alpha_composite(body_layer)
    d = ImageDraw.Draw(img)

    # ---------------------------------------------------------- clamp arms
    # Arms rise from the top of the body and hold the socks up in the air.
    draw_arm(d, (392, 372), (330, 150))
    draw_arm(d, (588, 372), (650, 150))
    draw_clamp(d, (330, 150))
    draw_clamp(d, (650, 150))

    # ---------------------------------------------------------- the socks
    # In front of the body, cuffs gripped by the clamps, feet dangling
    # free so the pair reads as socks at a glance.
    left_sock = make_sock(RED, scale=0.75)
    right_sock = make_sock(RED, scale=0.75, flip=True)
    left_sock = left_sock.rotate(7, expand=True, resample=Image.BICUBIC)
    right_sock = right_sock.rotate(-7, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(left_sock, (285, 152))
    img.alpha_composite(right_sock, (605, 152))
    d = ImageDraw.Draw(img)

    # Brand name, small and centred above the screen.
    brand = load_font(bold=True, size=30)
    label = "SOCKMATCH 3000"
    tw = d.textlength(label, font=brand)
    d.text(((252 + 728) / 2 - tw / 2, 388), label, font=brand, fill=INK)
    sub = load_font(size=15)
    sublabel = "A U T O M A T I C   S O C K   P A I R I N G   S Y S T E M"
    tw = d.textlength(sublabel, font=sub)
    d.text(((252 + 728) / 2 - tw / 2, 424), sublabel, font=sub, fill=SOFT)

    # ---------------------------------------------------------- the screen
    rrect(d, (292, 452, 566, 586), 18, fill=SCREEN, outline=(0, 0, 0), width=2)
    rrect(d, (300, 460, 558, 474), 8, fill=(255, 255, 255, 26))
    # Green glow behind the verdict.
    glow2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd2 = ImageDraw.Draw(glow2)
    gd2.ellipse([330, 470, 530, 560], fill=GREEN + (70,))
    img.alpha_composite(glow2.filter(ImageFilter.GaussianBlur(18)))
    d = ImageDraw.Draw(img)
    big = load_font(bold=True, size=52)
    verdict = "MATCH ✓"
    tw = d.textlength(verdict, font=big)
    d.text(((292 + 566) / 2 - tw / 2, 472), verdict, font=big, fill=GREEN)
    small = load_font(bold=True, size=24)
    found = "PAIR FOUND"
    tw = d.textlength(found, font=small)
    d.text(((292 + 566) / 2 - tw / 2, 536), found, font=small, fill=(200, 255, 220))

    # ---------------------------------------------------------- the dial
    cx, cy, r = 648, 519, 62
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 245, 243),
              outline=BODY_EDGE, width=3)
    d.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10],
              outline=(200, 198, 192), width=2)
    for i, ang in enumerate(range(-210, 31, 30)):
        a = math.radians(ang)
        x1 = cx + (r - 16) * math.cos(a)
        y1 = cy + (r - 16) * math.sin(a)
        x2 = cx + (r - 6) * math.cos(a)
        y2 = cy + (r - 6) * math.sin(a)
        col = GREEN_DK if i >= 5 else (150, 148, 142)
        d.line([(x1, y1), (x2, y2)], fill=col, width=4)
    # Needle parked in the green zone.
    a = math.radians(-30)
    d.line([(cx, cy), (cx + (r - 22) * math.cos(a), cy + (r - 22) * math.sin(a))],
           fill=RED, width=5)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=DARK)

    # Status LED + buttons under the screen.
    d.ellipse([306, 606, 322, 622], fill=GREEN)
    led_f = load_font(bold=True, size=16)
    d.text((330, 604), "READY", font=led_f, fill=INK)
    for i, label in enumerate(("SCAN", "PAIR", "FOLD")):
        x0 = 452 + i * 62
        rrect(d, (x0, 602, x0 + 52, 628), 10,
              fill=(238, 238, 236), outline=BODY_EDGE, width=2)
        bf = load_font(bold=True, size=13)
        tw = d.textlength(label, font=bf)
        d.text((x0 + 26 - tw / 2, 608), label, font=bf, fill=INK)
    # Model plate, bottom right of the face.
    plate = load_font(size=14)
    d.text((640, 668), "MODEL SM-3000", font=plate, fill=SOFT)
    d.text((640, 688), "110-240 V - 50/60 Hz", font=plate, fill=SOFT)

    # ---------------------------------------------------------- the accessory
    lone = make_flat_sock(BLUE)
    lone = lone.rotate(-12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(lone, (760, 786))

    # ---------------------------------------------------------- finish
    # Gentle vignette so the product stays the hero.
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-140, -140, W + 140, H + 140], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(180))
    dark = Image.new("RGBA", (W, H), (40, 34, 26, 42))
    img.paste(Image.composite(img, dark, vig), (0, 0))

    out = img.convert("RGB")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    out.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {out.size[0]}x{out.size[1]}, {size} bytes")
    assert out.size[0] <= 1024 and out.size[1] <= 1024
    assert size <= 1_048_576


if __name__ == "__main__":
    main()

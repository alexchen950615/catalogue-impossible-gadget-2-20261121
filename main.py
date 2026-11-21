#!/usr/bin/env python3
"""SockMatch 3000 — a catalogue photograph of an impossible gadget.

Draws, from scratch with PIL, a studio product shot of a small machine
that automatically pairs socks: two identical striped socks hang from
its twin clamp arms while its screen reads MATCH, and one lonely odd
sock lies on the floor beside it as the single accessory.

Output: /output/entry.png (1024x1024 PNG, < 1 MiB).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
OUT = "/output/entry.png"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# ---------------------------------------------------------------- palette
BG_TOP = (245, 243, 239)
BG_BOT = (214, 210, 203)
FLOOR_Y = 800
BODY = (248, 248, 246)
BODY_EDGE = (205, 205, 200)
BODY_SHADE = (228, 228, 224)
METAL = (176, 180, 186)
METAL_DARK = (120, 124, 130)
DARK = (32, 36, 42)
SCREEN = (24, 30, 36)
GREEN = (46, 204, 113)
GREEN_DIM = (28, 140, 78)
RED = (214, 64, 64)
BLUE = (66, 110, 190)
SOCK_WHITE = (250, 250, 248)
GREY_TEXT = (110, 110, 108)


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


# ---------------------------------------------------------------- backdrop
def backdrop():
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        # gentle vertical gradient, slightly warmer at the top
        r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
        g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
        b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    # soft radial studio glow behind the product
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse([180, 60, 844, 760], fill=42)
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img = Image.composite(
        Image.new("RGB", (W, H), (255, 255, 252)), img, glow)
    return img


def soft_shadow(base, box, blur, alpha):
    """Draw a blurred dark ellipse onto base (RGBA overlay)."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=(40, 36, 30, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(layer)


# ---------------------------------------------------------------- sock
def draw_sock(d, x, top_y, height, colour, stripe, foot_dir, scale=1.0):
    """A hanging sock: vertical tube, then a foot bending foot_dir (+1 right,
    -1 left). x is the centre of the tube; the cuff is at top_y."""
    w = int(74 * scale)
    leg_h = int(height * 0.62)
    foot_h = int(64 * scale)
    foot_len = int(96 * scale)
    # leg tube
    d.rounded_rectangle([x - w // 2, top_y, x + w // 2, top_y + leg_h + 10],
                        radius=int(20 * scale), fill=SOCK_WHITE,
                        outline=(190, 190, 186), width=2)
    # foot: horizontal rounded bar bending away from the leg
    foot_top = top_y + leg_h - 8
    fx0 = x if foot_dir > 0 else x - foot_len
    fx1 = x + foot_len if foot_dir > 0 else x
    d.rounded_rectangle([fx0, foot_top, fx1, foot_top + foot_h],
                        radius=int(20 * scale), fill=SOCK_WHITE,
                        outline=(190, 190, 186), width=2)
    # toe cap at the far end of the foot
    toe_cx = x + foot_dir * (foot_len - int(8 * scale))
    toe_cy = foot_top + foot_h // 2
    d.ellipse([toe_cx - int(18 * scale), toe_cy - int(20 * scale),
               toe_cx + int(18 * scale), toe_cy + int(20 * scale)],
              fill=colour)
    # cuff band + stripes on the leg
    d.rectangle([x - w // 2, top_y, x + w // 2, top_y + int(26 * scale)],
                fill=colour)
    for i, sy in enumerate((0.30, 0.45)):
        y0 = top_y + int(leg_h * sy)
        d.rectangle([x - w // 2, y0, x + w // 2, y0 + int(14 * scale)],
                    fill=stripe)
    # soft shading on the leg's outer edge
    sx0 = x + foot_dir * (w // 2 - 10)
    sx1 = x + foot_dir * (w // 2)
    d.rectangle([min(sx0, sx1), top_y + int(30 * scale),
                 max(sx0, sx1), top_y + leg_h],
                fill=(226, 226, 222))


def draw_flat_sock(d, cx, cy, angle, colour, stripe):
    """One lonely sock lying flat on the floor, rotated a little."""
    sock = Image.new("RGBA", (260, 120), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sock)
    # leg lying horizontally, foot pointing right-down
    sd.rounded_rectangle([10, 28, 170, 78], radius=22, fill=SOCK_WHITE,
                         outline=(190, 190, 186), width=2)
    sd.polygon([(150, 28), (210, 44), (238, 66), (228, 92), (196, 96),
                (150, 78)], fill=SOCK_WHITE, outline=(190, 190, 186))
    sd.ellipse([206, 62, 242, 98], fill=colour)  # toe
    sd.rectangle([10, 28, 44, 78], fill=colour)  # cuff
    for x0 in (78, 108):
        sd.rectangle([x0, 28, x0 + 13, 78], fill=stripe)
    sock = sock.rotate(angle, expand=True, resample=Image.BICUBIC)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base.alpha_composite(sock, (cx - sock.width // 2, cy - sock.height // 2))
    return base


# ---------------------------------------------------------------- device
def draw_device(img):
    d = ImageDraw.Draw(img)
    # ---- clamp arms (metal rods from the body top corners)
    for sgn in (-1, 1):
        x0 = 512 + sgn * 108
        x1 = 512 + sgn * 214
        d.line([x0, 400, x1, 318], fill=METAL_DARK, width=14)
        d.line([x0, 396, x1, 314], fill=METAL, width=7)
        # clamp jaws at the rod tip
        jx, jy = x1, 318
        d.rounded_rectangle([jx - 16, jy - 6, jx + 16, jy + 26], radius=7,
                            fill=METAL_DARK)
        d.rectangle([jx - 20, jy + 18, jx + 20, jy + 30], fill=DARK)
    # ---- hanging socks (the matched pair)
    draw_sock(d, 298, 344, 250, RED, RED, -1)
    draw_sock(d, 726, 344, 250, RED, RED, +1)
    # ---- body
    d.rounded_rectangle([384, 388, 640, 748], radius=40, fill=BODY,
                        outline=BODY_EDGE, width=3)
    # right-side shading + top highlight for a manufactured look
    d.rounded_rectangle([600, 388, 640, 748], radius=40, fill=BODY_SHADE)
    d.rounded_rectangle([384, 388, 640, 748], radius=40, outline=BODY_EDGE,
                        width=3)
    d.rounded_rectangle([396, 400, 628, 428], radius=14, fill=(255, 255, 255))
    # ---- screen
    d.rounded_rectangle([436, 428, 588, 500], radius=12, fill=SCREEN)
    f_big = font("DejaVuSans-Bold.ttf", 30)
    f_small = font("DejaVuSans.ttf", 17)
    d.text((512, 452), "MATCH ✓", font=f_big, fill=GREEN, anchor="mm")
    d.text((512, 482), "PAIR FOUND", font=f_small, fill=(150, 190, 165),
           anchor="mm")
    # ---- LED
    d.ellipse([600, 446, 622, 468], fill=GREEN)
    d.ellipse([604, 450, 618, 464], fill=(140, 255, 180))
    # ---- dial
    cx, cy, r = 512, 610, 58
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(236, 236, 233),
              outline=METAL_DARK, width=3)
    d.ellipse([cx - r + 12, cy - r + 12, cx + r - 12, cy + r - 12],
              fill=(250, 250, 248), outline=(200, 200, 196), width=2)
    for i in range(9):
        a = math.radians(210 + i * 30)
        x0 = cx + int(math.cos(a) * (r - 18))
        y0 = cy + int(math.sin(a) * (r - 18))
        x1 = cx + int(math.cos(a) * (r - 26))
        y1 = cy + int(math.sin(a) * (r - 26))
        d.line([x0, y0, x1, y1], fill=METAL_DARK, width=3)
    a = math.radians(300)
    d.line([cx, cy, cx + int(math.cos(a) * (r - 28)),
            cy + int(math.sin(a) * (r - 28))], fill=RED, width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=DARK)
    # ---- brand label
    f_brand = font("DejaVuSans-Bold.ttf", 22)
    d.text((512, 706), "SOCKMATCH 3000", font=f_brand, fill=GREY_TEXT,
           anchor="mm")
    # ---- feet
    d.rounded_rectangle([420, 748, 468, 766], radius=6, fill=DARK)
    d.rounded_rectangle([556, 748, 604, 766], radius=6, fill=DARK)


def main():
    img = backdrop().convert("RGBA")
    # floor shadows first
    soft_shadow(img, [220, 756, 804, 812], 18, 90)
    soft_shadow(img, [760, 800, 980, 836], 10, 70)
    # lonely odd sock (the accessory) lying on the floor, right side
    img.alpha_composite(draw_flat_sock(ImageDraw.Draw(img), 872, 806, -8,
                                       BLUE, BLUE))
    draw_device(img)
    img = img.convert("RGB")
    os.makedirs("/output", exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}: {img.size}, {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()

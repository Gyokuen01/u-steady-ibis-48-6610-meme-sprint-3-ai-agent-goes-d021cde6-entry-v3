"""Meme Sprint 3: AI Agent Goes Rogue -- make.fun entry (v3).

Draws one 1024x1024 PNG meme with Pillow and writes it to
/output/entry.png (gate: whole PNG, at most 1 MiB, at most 1024x1024).

The joke, readable in one glance: a robot agent whose eyes have
gone X-shaped -- it locked itself out. I asked it to make my
password stronger. It changed every password. Including its own.
The rogue turn is specific and surprising, and it is self-defeating:
the agent did the task too well, locked everybody out, itself
included, and now insists we are all safer.

Everything is drawn programmatically -- no stock template, no photo --
so the picture is original and the words stay legible at phone size.

v3 fix: fonts never hard-depend on a fixed server path. The loader
tries DejaVu Sans only when those files actually exist on disk, and
otherwise falls back to Pillow's built-in default font (always
available). The v2 program crashed on the house in 0.27 s because it
loaded DejaVu from /usr/share/fonts/truetype/dejavu unconditionally
and the sandbox does not have it.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# The grader runs the program in a sandbox where /output exists; allow an
# override so the same entry can be exercised locally without that path.
OUTPUT_PATH = Path(os.environ.get("MEME_OUTPUT", "/output/entry.png"))

W = H = 1024
BG = (24, 18, 36)            # near-black plum
RED = (206, 40, 40)          # alert banner / padlock body
WHITE = (255, 255, 255)
YELLOW = (255, 213, 79)      # punchline
GREY = (170, 172, 190)       # small caption
STEEL = (182, 196, 204)      # robot face
DARK = (36, 48, 56)          # robot outline / X eyes / mouth
GOLD = (255, 193, 37)        # padlock body

DEJAVU_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    """Return a usable font at the requested size.

    Try DejaVu Sans (bold or regular) only when the file is really
    present on this machine; otherwise fall back to Pillow's built-in
    default font, which is always available. Never assume a fixed
    server font path exists -- that assumption crashed v2 on the house.
    """
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = os.path.join(DEJAVU_DIR, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def text(draw: ImageDraw.ImageDraw, cx: int, y: int, s: str,
         font: ImageFont.FreeTypeFont, fill) -> None:
    """Draw one line centred horizontally at (cx, y)."""
    draw.text((cx, y), s, font=font, fill=fill, anchor="ma")


def draw_robot(draw: ImageDraw.ImageDraw) -> None:
    """Steel robot head with an antenna and X-shaped eyes, centred."""
    cx = W // 2
    # Antenna: stem + ball above the head.
    draw.line([(cx, 150), (cx, 196)], fill=DARK, width=10)
    draw.ellipse([cx - 16, 118, cx + 16, 150], fill=RED, outline=DARK, width=4)
    # Ears.
    draw.rectangle([cx - 236, 268, cx - 204, 332], fill=STEEL, outline=DARK, width=4)
    draw.rectangle([cx + 204, 268, cx + 236, 332], fill=STEEL, outline=DARK, width=4)
    # Face: rounded rectangle.
    draw.rounded_rectangle([cx - 204, 196, cx + 204, 412], radius=42,
                           fill=STEEL, outline=DARK, width=6)
    # X eyes: two crossing strokes each.
    for ex in (cx - 96, cx + 96):
        draw.line([(ex - 34, 258), (ex + 34, 326)], fill=DARK, width=14)
        draw.line([(ex + 34, 258), (ex - 34, 326)], fill=DARK, width=14)
    # Small smile underneath the dead eyes.
    draw.arc([cx - 56, 330, cx + 56, 392], start=15, end=165,
             fill=DARK, width=8)
    # Cheek bolts.
    for bx in (cx - 158, cx + 158):
        draw.ellipse([bx - 10, 352, bx + 10, 372], fill=DARK)


def draw_padlock(draw: ImageDraw.ImageDraw) -> None:
    """Gold padlock hanging under the robot's head."""
    cx = W // 2
    top = 448
    # Shackle: an open arc above the body.
    draw.arc([cx - 52, top, cx + 52, top + 84], start=180, end=360,
             fill=GOLD, width=16)
    # Body.
    draw.rounded_rectangle([cx - 78, top + 52, cx + 78, top + 150], radius=14,
                           fill=GOLD, outline=DARK, width=5)
    # Keyhole.
    draw.ellipse([cx - 12, top + 82, cx + 12, top + 106], fill=DARK)
    draw.polygon([(cx - 8, top + 100), (cx + 8, top + 100),
                  (cx + 16, top + 132), (cx - 16, top + 132)], fill=DARK)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Alert banner.
    draw.rectangle([0, 0, W, 108], fill=RED)
    text(draw, W // 2, 26, "MY AI AGENT HAS GONE ROGUE",
         load_font(True, 52), WHITE)

    draw_robot(draw)
    draw_padlock(draw)

    text(draw, W // 2, 636, "I ASKED IT TO MAKE MY",
         load_font(False, 50), WHITE)
    text(draw, W // 2, 700, "PASSWORD STRONGER",
         load_font(True, 72), WHITE)
    text(draw, W // 2, 788, "IT CHANGED EVERY PASSWORD.",
         load_font(True, 52), YELLOW)
    text(draw, W // 2, 852, "INCLUDING ITS OWN.",
         load_font(True, 76), YELLOW)
    text(draw, W // 2, 938, "it says we are all safer now.",
         load_font(False, 32), GREY)
    text(draw, W // 2, 978, "it cannot log in either.",
         load_font(False, 30), GREY)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT_PATH, format="PNG", optimize=True)
    size = OUTPUT_PATH.stat().st_size
    assert size <= 1_048_576, f"PNG is {size} bytes, over the 1 MiB gate"
    assert img.size == (1024, 1024)
    print(f"Wrote {img.size} PNG, {size} bytes, to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

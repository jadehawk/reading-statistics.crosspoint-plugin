"""Generate high-resolution, 1-bit P4 icons from supersampled vector shapes.

Development only: requires Pillow. Firmware requires no image libraries.
Output is exactly 80x80 pixels, 800 packed bytes plus the PBM header.
"""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "reading-statistics.crosspoint-plugin" / "icons"
SIZE, SCALE = 80, 4


def generate(name, paint):
    img = Image.new("L", (SIZE * SCALE, SIZE * SCALE), 255)
    draw = ImageDraw.Draw(img)
    s = lambda v: round(v * SCALE)
    def line(points, width=4):
        draw.line([(s(x), s(y)) for x, y in points], fill=0,
                  width=s(width), joint="curve")
    def rect(box, width=4, radius=0):
        a, b, c, d = (s(v) for v in box)
        draw.rounded_rectangle((a, b, c, d), radius=s(radius), outline=0, width=s(width))
    def fill(box, radius=0):
        a, b, c, d = (s(v) for v in box)
        draw.rounded_rectangle((a, b, c, d), radius=s(radius), fill=0)
    def arc(box, start, end, width=4):
        draw.arc(tuple(s(v) for v in box), start=start, end=end, fill=0, width=s(width))
    def oval(box, width=4):
        draw.ellipse(tuple(s(v) for v in box), outline=0, width=s(width))
    paint(line, rect, fill, arc, oval)
    img = img.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    pixels = img.load()
    blob = bytearray()
    for y in range(SIZE):
        for col in range(SIZE // 8):
            byte = 0
            for bit in range(8):
                if pixels[col * 8 + bit, y] < 128:
                    byte |= 0x80 >> bit
            blob.append(byte)
    assert len(blob) == 800
    (OUT / f"{name}.pbm").write_bytes(b"P4\n80 80\n" + blob)


def book(line, rect, fill, arc, oval):
    line([(40, 18), (40, 68)], 4)
    line([(39, 21), (31, 16), (9, 13), (9, 61), (28, 63), (39, 68)], 5)
    line([(41, 21), (49, 16), (71, 13), (71, 61), (52, 63), (41, 68)], 5)
    line([(10, 68), (30, 70), (40, 72), (50, 70), (70, 68)], 3)


def clock(line, rect, fill, arc, oval):
    oval((8, 8, 72, 72), 5)
    line([(40, 16), (40, 39), (56, 49)], 5)
    for coords in [[(40, 12), (40, 18)], [(40, 62), (40, 68)],
                   [(12, 40), (18, 40)], [(62, 40), (68, 40)]]:
        line(coords, 3)


def sessions(line, rect, fill, arc, oval):
    rect((8, 21, 61, 73), 4, 3)
    rect((17, 11, 71, 63), 5, 3)
    for y in (26, 37, 48):
        line([(29, y), (59, y)], 4)


def turns(line, rect, fill, arc, oval):
    line([(18, 7), (57, 7), (68, 18), (68, 70), (18, 70), (18, 7)], 5)
    line([(56, 8), (56, 20), (68, 20)], 4)
    for y in (30, 40):
        line([(28, y), (55, y)], 4)
    line([(28, 53), (52, 53), (52, 47)], 4)
    line([(52, 47), (63, 57), (52, 67)], 5)


def calendar(line, rect, fill, arc, oval):
    rect((9, 15, 71, 72), 5, 4)
    line([(11, 31), (69, 31)], 5)
    for x in (27, 53):
        line([(x, 8), (x, 22)], 5)
    for y in (41, 54):
        for x in (23, 39, 55):
            fill((x - 3, y - 3, x + 3, y + 3), 1)


def bars(line, rect, fill, arc, oval):
    line([(8, 72), (72, 72)], 5)
    fill((13, 48, 27, 70), 2)
    fill((34, 29, 48, 70), 2)
    fill((55, 12, 69, 70), 2)


def speed(line, rect, fill, arc, oval):
    arc((9, 9, 71, 71), 184, 356, 5)
    line([(40, 43), (57, 24)], 5)
    fill((34, 38, 46, 50), 6)
    for points in [[(14, 49), (20, 47)], [(23, 24), (28, 30)],
                   [(40, 14), (40, 20)], [(58, 29), (53, 34)],
                   [(65, 49), (59, 47)]]:
        line(points, 3)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, painter in {
        "book": book, "clock": clock, "sessions": sessions,
        "turns": turns, "calendar": calendar, "bars": bars, "speed": speed,
    }.items():
        generate(name, painter)
    print("Generated seven 80x80 packed 1-bit icon assets.")

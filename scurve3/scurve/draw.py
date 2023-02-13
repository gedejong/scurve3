import math
from typing import List

import cairo
from cairo import Antialias


class Canvas:
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)

    def ctx(self) -> cairo.Context:
        return cairo.Context(self.surface)

    def background(self, r: float, g: float, b: float, a: float = 1.0):
        c = self.ctx()
        c.set_source_rgba(r, g, b, a)
        c.rectangle(0, 0, self.width, self.height)
        c.fill()
        c.stroke()

    def save(self, fname: str):
        self.surface.write_to_png(fname)


def parse_color(c: str) -> List[float]:
    """
    Parse an HTML-style color specification
    """
    if len(c) == 6:
        r = int(int(c[0:2], 16) / 255.0)
        g = int(int(c[2:4], 16) / 255.0)
        b = int(int(c[4:6], 16) / 255.0)
        return [r, g, b]
    elif len(c) == 3:
        return c


class Demo:
    """
    Draws a 2d curve within a specified square.
    """

    PAD = 5

    def __init__(
        self, curve, size: int, color: str, background: str, dotsize: float, *marks
    ):
        self.curve = curve
        self.size, self.color, self.dotsize = size, color, dotsize
        self.background = background
        self.c = Canvas(size + self.PAD * 2, size + self.PAD * 2)
        self.c.background(*parse_color(self.background))
        self.ctx = self.c.ctx()
        self.ctx.set_line_width(1)
        # Assuming all dimension sizes are equal
        self.length = self.curve.dimensions()[0]
        self.marks = set(marks)
        self.scale = float(size) / (self.length - 1)

    def _coordinates(self):
        for x, y in self.curve:
            x = x * self.scale
            y = y * self.scale
            assert (
                x <= self.size
            ), f"""x smaller or equal than {self.size} expected,
                   got: {x} (scale: {self.scale})"""
            assert (
                y <= self.size
            ), f"""y smaller or equal than {self.size} expected,
                    got: {y} (scale: {self.scale})"""
            yield x + self.PAD, y + self.PAD

    def draw(self):
        self.ctx.move_to(self.PAD, self.PAD)
        off = 0
        lst = list(self._coordinates())
        for x, y in lst:
            if off in self.marks:
                self.ctx.set_source_rgba(1, 0, 0, 0.8)
                self.ctx.arc(x, y, self.dotsize * 2, 0, math.pi * 2)
                self.ctx.fill()
            else:
                self.ctx.set_source_rgba(1, 0, 0, 0.5)
                self.ctx.arc(x, y, self.dotsize, 0, math.pi * 2)
                self.ctx.fill()
            off += 1

        self.ctx.set_source_rgb(*parse_color(self.color))
        self.ctx.move_to(self.PAD, self.PAD)
        for x, y in lst:
            self.ctx.line_to(x, y)
        self.ctx.stroke()

    def save(self, fname):
        self.c.save(fname)


class Curve:
    def __init__(self, curve, size, background="FFFFFF", color="000000"):
        """
        size:  X and Y dimensions of image.
        """
        self.curve, self.size = curve, size
        self.background = parse_color(background)
        self.color = color

        self.order = 1
        while 2 ** (2 * (self.order + 1)) <= len(curve):
            self.order += 1

        self.c = Canvas(self.size, self.size)

        bkg = self.background + [1]
        self.c.background(*bkg)
        self.ctx = self.c.ctx()
        self.ctx.set_source_rgb(*parse_color(color))
        self.ctx.set_antialias(Antialias.GOOD)

        # Effective granularity
        self.bucket = int(len(curve) / ((2**self.order) ** 2))

    def pixel(self, n, color=None):
        if color and color != self.color:
            self.ctx.set_source_rgb(*parse_color(color))
            self.color = color
        x, y = self.curve.point(int(n / float(self.bucket)))
        self.ctx.rectangle(x, y, 1, 1)
        self.ctx.fill()

    def pixel_range(self, start, end):
        x = start - start % self.bucket
        while 1:
            self.pixel(x)
            if x >= end:
                break
            x += self.bucket

    def save(self, fname):
        self.c.save(fname)


class Swatch:
    def __init__(self, curve, colorwidth, height):
        """
        Color swatches from the RGB color cube.

        curve: A curve with dimension 3.
        colorwidth: Width of an individual color. Image width will be
        len(curve)*colorwidth.
        height: Height of the image
        """
        self.curve, self.colorwidth, self.height = curve, colorwidth, height
        self.c = Canvas(len(self.curve) * colorwidth, self.height)
        self.ctx = self.c.ctx()
        self.ctx.set_antialias(Antialias.GOOD)

    def save(self, fname):
        d = float(self.curve.dimensions()[0])
        offset = 0
        for r, g, b in self.curve:
            self.ctx.set_source_rgb(r / d, g / d, b / d)
            self.ctx.rectangle(offset, 0, self.colorwidth, self.height)
            self.ctx.fill()
            offset += self.colorwidth
        self.c.save(fname)

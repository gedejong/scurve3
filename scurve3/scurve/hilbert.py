import math

from . import utils


def transform(entry, direction, width, x):
    assert x < 2**width
    assert entry < 2**width
    return utils.rrot((x ^ entry), direction + 1, width)


def itransform(entry, direction, width, x):
    """
    Inverse transform - we simply reverse the operations in transform.
    """
    assert x < 2**width
    assert entry < 2**width
    return utils.lrot(x, direction + 1, width) ^ entry
    # There is an error in the Hamilton paper's formulation of the inverse
    # transform in Lemma 2.12. The correct restatement as a transform is as follows:
    # return transform(rrot(entry, direction+1, width), width-direction-2, width, x)


def direction(x, n):
    assert x < 2**n
    if x == 0:
        return 0
    elif x % 2 == 0:
        return utils.tsb(x - 1, n) % n
    else:
        return utils.tsb(x, n) % n


def entry(x):
    return 0 if x == 0 else utils.graycode(round(2 * int(((x - 1) / 2))))


def hilbert_point(dimension, order, h):
    """
    Convert an index on the Hilbert curve of the specified dimension and
    order to a set of point coordinates.
    """
    #    The bit widths in this function are:
    #        p[*]  - order
    #        h     - order*dimension
    #        l     - dimension
    #        e     - dimension
    hwidth = order * dimension
    e, d = 0, 0
    p = [0] * dimension
    for i in range(order):
        w = utils.bitrange(h, hwidth, i * dimension, i * dimension + dimension)
        graycode_w = utils.graycode(w)
        graycode_w = itransform(e, d, dimension, graycode_w)
        for j in range(dimension):
            b = utils.bitrange(graycode_w, dimension, j, j + 1)
            p[j] = utils.setbit(p[j], order, i, b)
        e = e ^ utils.lrot(entry(w), d + 1, dimension)
        d = (d + direction(w, dimension) + 1) % dimension
    return p


def hilbert_index(dimension, order, p):
    h, e, d = 0, 0, 0
    for index in range(order):
        bitset = 0
        for x in range(dimension):
            b = utils.bitrange(p[dimension - x - 1], order, index, index + 1)
            bitset |= b << x
        bitset = transform(e, d, dimension, bitset)
        gray_code = utils.igraycode(bitset)
        e = e ^ utils.lrot(entry(gray_code), d + 1, dimension)
        d = (d + direction(gray_code, dimension) + 1) % dimension
        h = (h << dimension) | gray_code
    return h


class Hilbert:
    def __init__(self, dimension, order):
        self.dimension, self.order = dimension, order

    @classmethod
    def from_size(cls, dimension, size):
        """
        Size is the total number of points in the curve.
        """
        x = math.log(size, 2)
        if not float(x) / dimension == int(x) / dimension:
            raise ValueError(
                "Size does not fit Hilbert curve of dimension %s." % dimension
            )
        return Hilbert(dimension, int(x / dimension))

    def __len__(self):
        return 2 ** (self.dimension * self.order)

    def __getitem__(self, idx):
        if idx >= len(self):
            raise IndexError
        return self.point(idx)

    def dimensions(self):
        """
        Size of this curve in each dimension.
        """
        return [
            int(math.ceil(len(self) ** (1 / float(self.dimension))))
        ] * self.dimension

    def index(self, p):
        return hilbert_index(self.dimension, self.order, p)

    def point(self, idx):
        return hilbert_point(self.dimension, self.order, idx)

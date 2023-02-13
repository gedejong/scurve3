import math
from typing import List

"""
This module provides the natural order traversal class in a cube.
"""


class Natural:
    """
    A natural order traversal of the points in a cube. Each point is
    simply considered a digit in a number.
    """

    def __init__(self, dimension, size):
        """
        dimension: Number of dimensions
        size: The size in each dimension
        """
        self.dimension, self.size = int(dimension), int(size)

    @classmethod
    def from_size(cls, dimension, size):
        """
        size: total number of points in the curve.
        """
        x = math.ceil(math.pow(size, 1 / float(dimension)))
        if not x ** dimension == size:
            raise ValueError("Size does not fit a square curve.")
        return Natural(dimension, math.ceil(x))

    def __len__(self):
        return self.size ** self.dimension

    def __getitem__(self, idx):
        if idx >= len(self):
            raise IndexError
        return self.point(idx)

    def dimensions(self):
        """
        Size of this curve in each dimension.
        """
        return [self.size] * self.dimension

    def index(self, p: List[int]) -> int:
        """
        Calculate the index of the given point `p` in the `size`-dimensional space.

        In the case of a natural ordering, the index is calculated by treating each digit as a base-`size` digit in
        a `dimension`-digit number, where the rightmost digit has the least significance and the leftmost digit has the
        greatest significance.

        :param p: A list of `dimension` integers representing the coordinates of the point in the space.
        :return: The calculated index of the point `p`.
        """
        idx = 0
        for power, i in enumerate(p):
            power = self.dimension - power - 1
            idx += i * (self.size ** power)
        return idx

    def point(self, idx: int) -> List[int]:
        """
        Calculate the point in the `size`-dimensional space corresponding to the given index `idx`.

        The calculation is performed by treating `idx` as a base-`size` number with `dimension` digits, where each digit
        represents the coordinate of the point in a corresponding dimension.

        :param idx: The index of the point in the space.
        :return: A list of `dimension` integers representing the coordinates of the point in the space.
        """
        p = []
        for i in range(self.dimension - 1, -1, -1):
            v = idx / (self.size ** i)
            if i > 0:
                idx = idx - (self.size ** i) * v
            p.append(v)
        return p

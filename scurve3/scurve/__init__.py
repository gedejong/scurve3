from . import graycurve
from . import hcurve
from . import hilbert
from . import natural
from . import zigzag
from . import zorder

curve_map = {
    "hcurve": hcurve.Hcurve,
    "hilbert": hilbert.Hilbert,
    "zigzag": zigzag.ZigZag,
    "zorder": zorder.ZOrder,
    "natural": natural.Natural,
    "gray": graycurve.GrayCurve,
}
curves = curve_map.keys()


def from_size(curve, dimension, size):
    """
    A convenience function for creating a specified curve by specifying
    size and dimension. All curves implement this common interface.
    """
    return curve_map[curve].from_size(dimension, size)


def from_order(curve, dimension, order):
    """
    A convenience function for creating a specified curve by specifying
    order and dimension. All curves implement this common interface, but
    the meaning of "order" may differ for each curve.
    """
    return curve_map[curve](dimension, order)

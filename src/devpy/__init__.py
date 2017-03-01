
import devpy

from .log import autolog  # noqa
from .tb import color_traceback  # noqa

__version__ = "0.1.1"


def dev_mode(color_traceback=True, autolog=True):  # noqa
    if color_traceback:
        devpy.color_traceback()
    if autolog:
        return devpy.autolog()

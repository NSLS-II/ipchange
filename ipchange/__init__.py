# flake8: noqa
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .moxa.moxa import MoxaHTTP_2_2
from .axis.axis import AxisWebcam
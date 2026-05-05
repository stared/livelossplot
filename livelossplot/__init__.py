"""
.. include:: ../README.md
"""

from . import inputs, outputs
from .inputs import *
from .main_logger import MainLogger
from .plot_losses import PlotLosses
from .version import __version__

__all__ = [
    'MainLogger',
    'PlotLosses',
    'PlotLossesIgnite',
    'PlotLossesKeras',
    'PlotLossesKerasTF',
    'PlotLossesPoutyne',
    '__version__',
    'inputs',
    'outputs',
]

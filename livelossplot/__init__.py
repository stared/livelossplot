"""
.. include:: ../README.md
"""

import sys
import warnings
from importlib.util import find_spec

from .main_logger import MainLogger
from .plot_losses import PlotLosses
from . import inputs
from .inputs import *
from . import outputs
from .version import __version__

_input_plugin_dict = {
    'keras': 'Keras',
    'tf_keras': 'KerasTF',
    'pytorch_ignite': 'Ignite',
    'poutyne': 'Poutyne',
}


class OldDependenciesFinder:
    """
    Data package module loader finder. This class sits on `sys.meta_path` and returns the
    loader it knows for a given path, if it knows a compatible loader.
    """
    @classmethod
    def find_spec(self, fullname: str, *_, **__):
        """This functions is what gets executed by the loader.
        Args:
            fullname: name of the called module
        """
        parts = fullname.split('.')
        if len(parts) == 2 and parts[0] == 'livelossplot' and parts[1] in _input_plugin_dict:
            name = parts[1]
            msg = 'livelossplot.{name} will be deprecated, please use livelossplot.inputs.{name}\n'
            msg += 'or use callback directly: from livelossplot import PlotLosses{new_name}'
            warnings.warn(msg.format(name=name, new_name=_input_plugin_dict[name]), DeprecationWarning)
            fullname = 'livelossplot.inputs.{name}'.format(name=name)
            return find_spec(fullname)
        return None


sys.meta_path.append(OldDependenciesFinder())

__all__ = [
    'MainLogger', 'inputs', 'outputs', 'PlotLosses', 'PlotLossesKeras', 'PlotLossesKerasTF', 'PlotLossesIgnite',
    'PlotLossesPoutyne'
]

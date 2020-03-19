import sys
import warnings
from importlib.util import find_spec

from .main_logger import MainLogger
from .plot_losses import PlotLosses
from .version import __version__


SHORTEN_INPUT_PATHS = [
    'keras',
    'tf_keras',
    'pytorch_ignite',
]


def PlotLossesKeras(**kwargs):
    from .inputs.keras import PlotLossesCallback
    return PlotLossesCallback(**kwargs)


def PlotLossesTensorFlowKeras(**kwargs):
    from .inputs.tf_keras import PlotLossesCallback
    return PlotLossesCallback(**kwargs)


class OldDependenciesFinder:
    """
    Data package module loader finder. This class sits on `sys.meta_path` and returns the
    loader it knows for a given path, if it knows a compatible loader.
    """

    @classmethod
    def find_spec(self, fullname, *_, **__):
        """
        This functions is what gets executed by the loader.
        """
        parts = fullname.split('.')
        if len(parts) == 2 and parts[0] == 'livelossplot' and parts[1] in SHORTEN_INPUT_PATHS:
            warnings.warn(
                'livelossplot.{} will be deprecated, please use livelossplot.inputs.{}'.format(parts[1],
                                                                                                      parts[1]),
                DeprecationWarning
            )
            fullname = '.'.join(['livelossplot', 'inputs', parts[1]])
            return find_spec(fullname)
        return None


sys.meta_path.append(OldDependenciesFinder())

__all__ = ['PlotLosses']

import warnings
from .version import __version__

from .plot_losses import PlotLosses
from .main_logger import MainLogger

# TODO 
# expose keras as before, something like
# import livelossplot.input_plugins.keras as liveloss.keras
# or consider undepreciating lines below?

def PlotLossesKeras(*args, **kwargs):
    warnings.warn("From v0.3 onwards, use:\nfrom livelossplot.keras import PlotLossesCallback", DeprecationWarning)
    from .input_plugins.keras import PlotLossesCallback
    return PlotLossesCallback(*args, **kwargs)

def PlotLossesTensorFlowKeras(*args, **kwargs):
    warnings.warn("New and deprecated at the same time!\nFrom v0.3 onwards, use:\nfrom livelossplot.tf_keras import PlotLossesCallback", DeprecationWarning)
    from .input_plugins.tf_keras import PlotLossesCallback
    return PlotLossesCallback(*args, **kwargs)

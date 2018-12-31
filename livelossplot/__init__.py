import warnings
from .core import draw_plot
from .generic_plot import PlotLosses

# keras.PlotLossesCallback and pytoune.PlotLossesCallback
# NOT loaded, as they depend on other libraries

def PlotLossesKeras(*args, **kwargs):
    warnings.warn("Deprecation warning:\nFrom v0.3 onwards, use:\nfrom livelossplot.keras import PlotLossesCallback")
    from .keras import PlotLossesCallback
    return PlotLossesCallback(*args, **kwargs)

def PlotLossesPytoune(*args, **kwargs):
    warnings.warn("From v0.3 onwards, use:\nfrom livelossplot.pytoune import PlotLossesCallback", DeprecationWarning)
    from .pytoune import PlotLossesCallback
    return PlotLossesCallback(*args, **kwargs)

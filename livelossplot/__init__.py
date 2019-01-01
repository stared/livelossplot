import warnings
from .core import draw_plot
from .generic_plot import PlotLosses

# keras.PlotLossesCallback and pytoune.PlotLossesCallback
# NOT loaded, as they depend on other libraries

# open question: keep it as deprecated,
# or as an alternative (but legit) interface?

def PlotLossesKeras(*args, **kwargs):
    warnings.warn("From v0.3 onwards, use:\nfrom livelossplot.keras import PlotLossesCallback", DeprecationWarning)
    from .keras import PlotLossesCallback
    return PlotLossesCallback(*args, **kwargs)

def PlotLossesTensorFlowKeras(*args, **kwargs):
    warnings.warn("New and deprecated at the same time!\nFrom v0.3 onwards, use:\nfrom livelossplot.tf_keras import PlotLossesCallback", DeprecationWarning)
    from .tf_keras import PlotLossesCallback
    return PlotLossesCallback(*args, **kwargs)

def PlotLossesPytoune(*args, **kwargs):
    warnings.warn("From v0.3 onwards, use:\nfrom livelossplot.pytoune import PlotLossesCallback", DeprecationWarning)
    from .pytoune import PlotLossesCallback
    return PlotLossesCallback(*args, **kwargs)

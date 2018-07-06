from .core import draw_plot
from .generic_plot import PlotLosses

try:
    from .keras_plot import PlotLossesKeras
except ImportError:
    # import keras plot only if there is keras
    pass

try:
    from .pytoune_plot import PlotLossesPytoune
except ImportError:
    # import pytoune plot only if there is pytoune
    pass

from .core import draw_plot
from .generic_plot import PlotLosses
try:
    from .keras_plot import PlotLossesKeras
except:
    # import keras plot only if there is keras
    pass

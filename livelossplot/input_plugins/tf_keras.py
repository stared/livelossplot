from tensorflow import keras
from .generic_keras import _PlotLossesCallback


class PlotLossesCallback(_PlotLossesCallback, keras.callbacks.Callback):
    """Callback for tensorflow keras"""
    def __init__(self, **kwargs):
        keras.callbacks.Callback.__init__(self)
        _PlotLossesCallback.__init__(self, **kwargs)

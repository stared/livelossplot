from __future__ import absolute_import

import keras
from .generic_keras import _PlotLossesCallback

class PlotLossesCallback(_PlotLossesCallback, keras.callbacks.Callback):
    def __init__(self, **kwargs):
        keras.callbacks.Callback.__init__(self)
        _PlotLossesCallback.__init__(self, **kwargs)

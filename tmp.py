from time import sleep
import numpy as np

from livelossplot.plot_losses import PlotLosses
from livelossplot.outputs import BokehPlot

#%%

liveplot = PlotLosses(outputs=[BokehPlot()], mode='script')

for i in range(10):
    liveplot.update(
        {
            'acc': 1 - np.random.rand() / (i + 2.),
            'val_acc': 1 - np.random.rand() / (i + 0.5),
            'loss': 1. / (i + 2.),
            'val_loss': 1. / (i + 0.5),
            'mse': 1. / (i + 0.8),
            'val_mse': 1. / (i + 0.7),
            'lr': 0.01
        }
    )
    liveplot.send()
    sleep(.1)

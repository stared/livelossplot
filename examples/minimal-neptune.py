# TO START:
# pip install livelossplot
# pip install neptune-cli
# neptune account login
# neptune run minimal-neptune.py
# enjoy results

from time import sleep
import numpy as np

from livelossplot.generic_plot import PlotLosses

liveplot = PlotLosses(target='neptune')
for i in range(20):
    liveplot.update({
        'accuracy': 1 - np.random.rand() / (i + 2.),
        'val_accuracy': 1 - np.random.rand() / (i + 0.5),
        'mse': 1. / (i + 2.),
        'val_mse': 1. / (i + 0.5)
    })
    liveplot.draw()
    sleep(.5)

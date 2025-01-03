# from livelossplot 0.5.6

from time import sleep
import numpy as np
from livelossplot import PlotLosses

plotlosses = PlotLosses(mode="script")

for i in range(10):
    plotlosses.update(
        {
            "acc": 1 - np.random.rand() / (i + 2.0),
            "val_acc": 1 - np.random.rand() / (i + 0.5),
            "loss": 1.0 / (i + 2.0),
            "val_loss": 1.0 / (i + 0.5),
        }
    )
    plotlosses.send()
    sleep(0.5)

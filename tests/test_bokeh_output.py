import os

import numpy as np

from livelossplot import PlotLosses
from livelossplot.outputs import BokehPlot


def test_bokeh_plot():
    logger = BokehPlot()

    liveplot = PlotLosses(outputs=[logger], mode='script')

    for i in range(3):
        liveplot.update(
            {
                'acc': 1 - np.random.rand() / (i + 2.),
                'val_acc': 1 - np.random.rand() / (i + 0.5),
                'loss': 1. / (i + 2.),
                'val_loss': 1. / (i + 0.5)
            }
        )
        liveplot.send()

    assert os.path.isfile(logger.output_file)

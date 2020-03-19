import os

import numpy as np

from livelossplot import plot_losses
from livelossplot.outputs import tensorboard


def test_tensorboard():
    groups = {'acccuracy': ['acc', 'val_acc'], 'log-loss': ['loss', 'val_loss']}
    logger = tensorboard.TensorboardLogger()

    liveplot = plot_losses.PlotLosses(groups=groups, outputs=(logger, ))

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

    assert all([f.startswith('events.out.tfevents.') for f in os.listdir(logger._path)])

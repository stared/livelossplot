# TO START:
# pip install livelossplot
# pip install neptune-client
# export environment variables
# enjoy results

import os
from time import sleep

import numpy as np

from livelossplot.output_plugins.neptune import NeptuneLogger
from livelossplot.plot_losses import PlotLosses


def main():
    api_token = os.environ.get('NEPTUNE_API_TOKEN')
    project_qualified_name = os.environ.get('NEPTUNE_PROJECT_NAME')
    logger = NeptuneLogger(api_token=api_token, project_qualified_name=project_qualified_name)
    liveplot = PlotLosses(outputs=[logger])
    for i in range(20):
        liveplot.update({
            'accuracy': 1 - np.random.rand() / (i + 2.),
            'val_accuracy': 1 - np.random.rand() / (i + 0.5),
            'mse': 1. / (i + 2.),
            'val_mse': 1. / (i + 0.5)
        })
        liveplot.send()
        sleep(.5)


if __name__ == '__main__':
    main()

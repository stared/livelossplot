# TO START:
# pip install neptune, livelossplot
# export environment variables
# enjoy results

import os
from time import sleep

import numpy as np

from livelossplot.outputs import NeptuneLogger
from livelossplot import PlotLosses


def main():
    api_token = os.environ.get("NEPTUNE_API_TOKEN")
    project_qualified_name = os.environ.get("NEPTUNE_PROJECT")
    logger = NeptuneLogger(
        api_token=api_token,
        project_qualified_name=project_qualified_name,
        tags=["example", "livelossplot"],
    )
    liveplot = PlotLosses(outputs=[logger])
    for i in range(20):
        liveplot.update(
            {
                "accuracy": 1 - np.random.rand() / (i + 2.0),
                "val_accuracy": 1 - np.random.rand() / (i + 0.5),
                "mse": 1.0 / (i + 2.0),
                "val_mse": 1.0 / (i + 0.5),
            }
        )
        liveplot.send()
        sleep(0.5)


if __name__ == "__main__":
    main()

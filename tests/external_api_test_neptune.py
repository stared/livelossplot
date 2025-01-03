import numpy as np

from livelossplot import PlotLosses
from livelossplot.outputs import NeptuneLogger

import neptune


def test_neptune():
    neptune_logger = NeptuneLogger(
        api_token="ANONYMOUS",
        project_qualified_name="shared/colab-test-run",
        tags=["livelossplot", "github-actions"],
    )

    plotlosses = PlotLosses(outputs=[neptune_logger])

    assert neptune_logger.run.exists

    for i in range(3):
        plotlosses.update(
            {
                "acc": 1 - np.random.rand() / (i + 2.0),
                "val_acc": 1 - np.random.rand() / (i + 0.5),
                "loss": 1.0 / (i + 2.0),
                "val_loss": 1.0 / (i + 0.5),
            }
        )
        plotlosses.send()

    assert neptune_logger.run.exists

    neptune_logger.close()

    # Get the run URL
    url = neptune_logger.run.get_url()

    assert len(url) > 0

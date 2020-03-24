import numpy as np

from livelossplot import PlotLosses
from livelossplot.outputs import NeptuneLogger

import neptune


def test_neptune():
    neptune_logger = NeptuneLogger(
        api_token="ANONYMOUS", project_qualified_name="shared/colab-test-run", tags=['livelossplot', 'github-actions']
    )

    plotlosses = PlotLosses(outputs=[neptune_logger])

    assert neptune_logger.experiment.state == 'running'

    for i in range(3):
        plotlosses.update(
            {
                'acc': 1 - np.random.rand() / (i + 2.),
                'val_acc': 1 - np.random.rand() / (i + 0.5),
                'loss': 1. / (i + 2.),
                'val_loss': 1. / (i + 0.5)
            }
        )
        plotlosses.send()

    assert neptune_logger.experiment.state == 'running'

    neptune_logger.stop()

    assert neptune_logger.experiment.state == 'succeed'

    url = neptune.project._get_experiment_link(neptune_logger.experiment)

    assert len(url) > 0

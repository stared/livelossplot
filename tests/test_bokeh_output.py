from pathlib import Path

import numpy as np

from livelossplot import PlotLosses
from livelossplot.outputs import BokehPlot


def test_bokeh_plot(tmp_path: Path) -> None:
    output_file = tmp_path / "bokeh_output.html"
    plot = BokehPlot(output_file=str(output_file), auto_open=False)
    liveplot = PlotLosses(outputs=[plot], mode='script')

    rng = np.random.default_rng(0)
    for i in range(3):
        liveplot.update({
            'acc': 1 - rng.random() / (i + 2.0),
            'val_acc': 1 - rng.random() / (i + 0.5),
            'loss': 1.0 / (i + 2.0),
            'val_loss': 1.0 / (i + 0.5),
        })
        liveplot.send()

    assert output_file.is_file()
    content = output_file.read_text()
    assert output_file.stat().st_size > 0
    assert 'bokeh' in content.lower()
    assert '<script' in content

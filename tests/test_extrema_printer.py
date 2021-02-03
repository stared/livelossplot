from livelossplot import PlotLosses
from livelossplot.outputs import ExtremaPrinter


def test_extrema_print():
    """Test if plugin object cache contains valid values"""
    groups = {'accuracy': ['acc', 'val_acc'], 'log-loss': ['loss', 'val_loss']}
    plugin = ExtremaPrinter()
    outputs = (plugin, )
    liveplot = PlotLosses(outputs=outputs, groups=groups)
    liveplot.update({'acc': 0.5, 'val_acc': 0.4, 'loss': 1.2, 'val_loss': 1.1})
    liveplot.update({'acc': 0.55, 'val_acc': 0.45, 'loss': 1.1, 'val_loss': 1.0})
    liveplot.update({'acc': 0.65, 'val_acc': 0.35, 'loss': 0.5, 'val_loss': 0.9})
    liveplot.update({'acc': 0.65, 'val_acc': 0.55, 'loss': 1.0, 'val_loss': 0.9})
    liveplot.send()
    message = liveplot.outputs[0].last_message
    ref_message = '\n'.join(
        [
            'accuracy', '\ttraining         \t (min:    0.500, max:    0.650, cur:    0.650)',
            '\tvalidation       \t (min:    0.350, max:    0.550, cur:    0.550)', 'log-loss',
            '\ttraining         \t (min:    0.500, max:    1.200, cur:    1.000)',
            '\tvalidation       \t (min:    0.900, max:    1.100, cur:    0.900)'
        ]
    )
    assert message == ref_message

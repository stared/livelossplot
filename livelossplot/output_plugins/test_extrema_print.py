from livelossplot.plot_losses import PlotLosses
from . import extrema_print


def test_extrema_print():
    """Test if plugin object cache contains valid values"""
    groups = {'acccuracy': ['acc', 'val_acc'], 'log-loss': ['loss', 'val_loss']}
    plugin = extrema_print.ExtremaPrint()
    outputs = (plugin, )
    liveplot = PlotLosses(outputs=outputs, groups=groups)
    liveplot.update({'acc': 0.5, 'val_acc': 0.4, 'loss': 1.2, 'val_loss': 1.1})
    liveplot.update({'acc': 0.55, 'val_acc': 0.45, 'loss': 1.1, 'val_loss': 1.0})
    liveplot.update({'acc': 0.65, 'val_acc': 0.35, 'loss': 0.5, 'val_loss': 0.9})
    liveplot.update({'acc': 0.65, 'val_acc': 0.55, 'loss': 1.0, 'val_loss': 0.9})
    liveplot.send()
    assert len(plugin.extrema_cache['loss']) == 3
    assert plugin.extrema_cache['val_acc']['min'] == 0.35
    assert plugin.extrema_cache['val_acc']['max'] == 0.55
    assert plugin.extrema_cache['val_acc']['current'] == 0.55

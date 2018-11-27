from __future__ import division

from keras.callbacks import Callback
from .generic_plot import PlotLosses

metric2printable = {
    "acc": "Accuracy",
    "mean_squared_error": "Mean squared error",
    "mean_absolute_error": "Mean absolute error",
    "mean_absolute_percentage_error": "Mean absolute percentage error",
    # etc
    "categorical_crossentropy": "Log-loss",
    "sparse_categorical_crossentropy": "Log-loss",
    "binary_crossentropy": "Log-loss",
    "kullback_leibler_divergence": "Log-loss"
}


def loss2name(loss):
    if hasattr(loss, '__call__'):
        # if passed as a function
        return loss.__name__
    else:
        # if passed as a string
        return loss


class PlotLossesKeras(Callback):
    def __init__(self, **kwargs):
        super(PlotLossesKeras, self).__init__()
        self.liveplot = PlotLosses(**kwargs)

    def on_train_begin(self, logs={}):
        self.liveplot.set_metrics([
            metric for metric in self.params['metrics']
            if not metric.startswith('val_')
        ])

        # slightly convolved due to model.complie(loss=...) stuff
        # vide https://github.com/keras-team/keras/blob/master/keras/engine/training.py
        if isinstance(self.model.loss, list):
            losses = self.model.loss
        elif isinstance(self.model.loss, dict):
            losses = list(self.model.loss.values())
        else:
            # by far the most common scenario
            losses = [self.model.loss]

        metric2printable_updated = metric2printable.copy()
        loss_name = loss2name(losses[0])
        metric2printable_updated['loss'] =\
            "{} (cost function)".format(metric2printable_updated.get(loss_name, loss_name))

        if len(losses) > 1:
            for output_name, loss in zip(self.model.output_names, losses):
                loss_name = loss2name(loss)
                metric2printable_updated['{}_loss'.format(output_name)] =\
                    "{} ({})".format(metric2printable_updated.get(loss_name, loss_name), output_name)
        else:
            for output_name in self.model.output_names:
                metric2printable_updated['{}_loss'.format(output_name)] =\
                    "{} ({})".format(metric2printable_updated.get(loss_name, loss_name), output_name)

        self.liveplot.metric2title = metric2printable_updated
        self.liveplot.max_epoch = self.params['epochs']

    def on_epoch_end(self, epoch, logs={}):
        self.liveplot.update(logs.copy())
        self.liveplot.draw()

from __future__ import division
import math

from .core import draw_plot, not_inline_warning


def _is_unset(metric):
    return metric is None or math.isnan(metric)

def _validate_training_size(samples_per_update, training_size):
    if samples_per_update is not None and training_size is None:
        raise ValueError("Parameter 'training_size' is required if 'samples_per_update' is provided.")


class PlotLosses():
    def __init__(self, figsize=None, cell_size=(6, 4), dynamic_x_axis=False, max_cols=2,
                 max_epoch=None, metric2title={}, validation_fmt="val_{}", plot_extrema=True, fig_path=None,
                 samples_per_update = None, training_size = None):
        self.figsize = figsize
        self.cell_size = cell_size
        self.dynamic_x_axis = dynamic_x_axis
        self.max_cols = max_cols
        self.max_epoch = max_epoch
        self.metric2title = metric2title
        self.validation_fmt = validation_fmt
        self.logs = None
        self.base_metrics = None
        self.metrics_extrema = None
        self.plot_extrema = plot_extrema
        self.fig_path = fig_path
        self.training_size = training_size
        self.samples_per_update = samples_per_update
        self.batch_size = None

        self.set_max_epoch(max_epoch)
        not_inline_warning()
        _validate_training_size(samples_per_update, training_size)

    def set_max_epoch(self, max_epoch):
        self.max_epoch = max_epoch if not self.dynamic_x_axis else None

    def set_metrics(self, metrics):
        self.base_metrics = metrics
        if self.plot_extrema:
            self.metrics_extrema = {
                ftm.format(metric): {
                    'min': None,
                    'max': None,
                }
                for metric in metrics
                for ftm in ['{}', self.validation_fmt]
            }
        if self.figsize is None:
            self.figsize = (
                self.max_cols * self.cell_size[0],
                ((len(self.base_metrics) + 1) // self.max_cols + 1) * self.cell_size[1]
            )

        self.logs = {"epoch":[],"batch":[]}

    def _format_metric_name(self, metric_name):
        if 'val' not in metric_name:
            return metric_name
        return metric_name.replace('validation_', 'val_')  # this should be more generic

    def _update_extrema(self, log):
        for metric, value in log.items():
            formatted_name = self._format_metric_name(metric)
            extrema = self.metrics_extrema[formatted_name]
            if _is_unset(extrema['min']) or value < extrema['min']:
                extrema['min'] = float(value)
            if _is_unset(extrema['max']) or value > extrema['max']:
                extrema['max'] = float(value)
    def _set_batch_size(self, batch_size):
        if self.batch_size is not None:
            return
        else:
            if batch_size > self.samples_per_update:
                raise ValueError(
                    "samples_per_update should be equal to or greater than batch size.\n \
                    samples_per_update ={samples_per_update}, batch_size={batch_size}".format(
                    samples_per_update = self.samples_per_update,
                    batch_size = batch_size
                    )
                )
            elif self.samples_per_update%batch_size != 0:
                raise ValueError(
                    "samples_per_update should be a multiple of batch size.\n \
                    samples_per_update ={samples_per_update}, batch_size={batch_size}".format(
                    samples_per_update = self.samples_per_update,
                    batch_size = batch_size
                    )
                )
            else:
                self.batch_size = batch_size



    def update(self, log, epoch_log=True):

        if "size" in log.keys() and self.samples_per_update is not None:
            self._set_batch_size(log["size"])

        unwanted_log_keys = ["size", "batch"]
        log = {x:y for x,y in log.items() if x not in unwanted_log_keys}
        if self.logs is None:
            self.set_metrics([
                metric for metric in log.keys()
                if 'val' not in metric.lower()
            ])

        if epoch_log:
            self.logs["epoch"].append(log)
        else:
            self.logs["batch"].append(log)

        if self.plot_extrema:
            self._update_extrema(log)

    def draw(self):
        draw_plot(self.logs, self.base_metrics,
                  figsize=self.figsize, max_epoch=self.max_epoch,
                  max_cols=self.max_cols,
                  validation_fmt=self.validation_fmt,
                  metric2title=self.metric2title,
                  extrema=self.metrics_extrema,
                  fig_path=self.fig_path,
                  samples_per_update = self.samples_per_update,
                  training_size=self.training_size,
                  batch_size = self.batch_size)

import matplotlib.pyplot as plt
from keras.callbacks import Callback
from IPython.display import clear_output
#from matplotlib.ticker import FormatStrFormatter

# TODO
# object-oriented API

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

class PlotLosses(Callback):
    def __init__(self, figsize=None, dynamic_x_axis=False):
        self.figsize = figsize
        self.dynamic_x_axis = dynamic_x_axis

    def on_train_begin(self, logs={}):

        self.base_metrics = [metric for metric in self.params['metrics'] if not metric.startswith('val_')]
        self.loss_metric = self.model.loss
        self.max_epoch = self.params['epochs']

        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)

        clear_output(wait=True)
        plt.figure(figsize=self.figsize)

        for metric_id, metric in enumerate(self.base_metrics):
            plt.subplot(1, len(self.base_metrics), metric_id + 1)

            if not self.dynamic_x_axis:
                plt.xlim(xmax=self.max_epoch)

            plt.plot(range(1, len(self.logs) + 1),
                     [log[metric] for log in self.logs],
                     label="training")
            if self.params['do_validation']:
                plt.plot(range(1, len(self.logs) + 1),
                         [log['val_' + metric] for log in self.logs],
                         label="validation")
            if metric == 'loss':
                plt.title(metric2printable.get(self.loss_metric, self.loss_metric) + " (cost function)")
            else:
                plt.title(metric2printable.get(metric, metric))

            plt.xlabel('epoch')
            plt.legend(loc='center right')

        plt.tight_layout()
        plt.show();

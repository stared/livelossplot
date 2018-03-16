import matplotlib.pyplot as plt
from keras.callbacks import Callback
from IPython.display import clear_output
#from matplotlib.ticker import FormatStrFormatter

# TODO
# object-oriented API

def translate_metric(x):
    translations = {'acc': "Accuracy", 'loss': "Log-loss (cost function)"}
    if x in translations:
        return translations[x]
    else:
        return x

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
    def __init__(self, figsize=None):
        #super(PlotLosses, self).__init__()
        self.figsize = figsize

    def on_train_begin(self, logs={}):

        self.base_metrics = [metric for metric in self.params['metrics'] if not metric.startswith('val_')]
        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)

        clear_output(wait=True)
        plt.figure(figsize=self.figsize)

        for metric_id, metric in enumerate(self.base_metrics):
            plt.subplot(1, len(self.base_metrics), metric_id + 1)

            plt.plot(range(1, len(self.logs) + 1),
                     [log[metric] for log in self.logs],
                     label="training")
            if self.params['do_validation']:
                plt.plot(range(1, len(self.logs) + 1),
                         [log['val_' + metric] for log in self.logs],
                         label="validation")
            plt.title(translate_metric(metric))
            plt.xlabel('epoch')
            plt.legend(loc='center right')

        plt.tight_layout()
        plt.show();

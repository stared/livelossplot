from typing import Literal, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


class BaseSubplot:
    def __init__(self):
        self.output_mode: Literal['notebook', 'script'] = 'notebook'

    def draw(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        self.draw(*args, **kwargs)

    def set_output_mode(self, mode: Literal['notebook', 'script']):
        self.output_mode = mode

    def _present(self, fig: plt.Figure):
        """Render fig appropriately for the current output mode."""
        if self.output_mode == 'notebook':
            try:
                from IPython.display import clear_output
                clear_output(wait=True)
            except ImportError:
                pass
            plt.show()
        else:
            plt.draw()
            plt.pause(0.05)


class LossSubplot(BaseSubplot):
    """To rewrire, this one now won't work"""
    def __init__(
        self, metric, title="", series_fmt={
            'training': '{}',
            'validation': 'val_{}'
        }, skip_first=2, max_epoch=None
    ):
        super().__init__()
        self.metric = metric
        self.title = title
        self.series_fmt = series_fmt
        self.skip_first = skip_first
        self.max_epoch = max_epoch
        raise NotImplementedError()

    def _how_many_to_skip(self, log_length, skip_first):
        if log_length < skip_first:
            return 0
        elif log_length < 2 * skip_first:
            return log_length - skip_first
        else:
            return skip_first

    def draw(self, logs):
        skip = self._how_many_to_skip(len(logs), self.skip_first)

        if self.max_epoch is not None:
            plt.xlim(1 + skip, self.max_epoch)

        for serie_label, serie_fmt in self.series_fmt.items():

            serie_metric_name = serie_fmt.format(self.metric)
            serie_metric_logs = [
                (log.get('_i', i + 1), log[serie_metric_name])
                for i, log in enumerate(logs[skip:]) if serie_metric_name in log
            ]

            if len(serie_metric_logs) > 0:
                xs, ys = zip(*serie_metric_logs)
                plt.plot(xs, ys, label=serie_label)

        plt.title(self.title)
        plt.xlabel('epoch')
        plt.legend(loc='center right')


class Plot1D(BaseSubplot):
    def __init__(self, model, X, Y):
        super().__init__()
        self.model = model
        self.X = X
        self.Y = Y

    def predict(self, model, X):
        # e.g. model(torch.fromnumpy(X)).detach().numpy()
        return model.predict(X)

    def draw(self, *args, **kwargs):
        plt.plot(self.X, self.Y, 'r.', label="Ground truth")
        plt.plot(self.X, self.predict(self.model, self.X), '-', label="Model")
        plt.title("Prediction")
        plt.legend(loc='lower right')


class Plot2d(BaseSubplot):
    def __init__(self, model, X, Y, valiation_data=(None, None), h=0.02, margin=0.25, device='cpu'):
        super().__init__()

        self.model = model
        self.X = X
        self.Y = Y
        self.X_test, self.Y_test = valiation_data

        self.cm_bg = plt.cm.RdBu
        self.cm_points = ListedColormap(['#FF0000', '#0000FF'])

        x_min = X[:, 0].min() - margin
        x_max = X[:, 0].max() + margin

        y_min = X[:, 1].min() - margin
        y_max = X[:, 1].max() + margin

        self.xx, self.yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        self.torch_device = device

        self._fig: Optional[plt.Figure] = None
        self._ax: Optional[plt.Axes] = None

    def _predict_pytorch(self, model, x_numpy):
        import torch
        x = torch.from_numpy(x_numpy).to(self.torch_device).float()
        return model(x).softmax(dim=1).detach().cpu().numpy()

    def predict(self, model, X):
        # e.g. model(torch.fromnumpy(X)).detach().numpy()
        return model.predict(X)

    def send(self, logger):
        if self._fig is None or not plt.fignum_exists(self._fig.number):
            self._fig, self._ax = plt.subplots()
        else:
            self._ax.clear()

        Z = self.predict(self.model, np.c_[self.xx.ravel(), self.yy.ravel()])[:, 1]
        Z = Z.reshape(self.xx.shape)
        self._ax.contourf(self.xx, self.yy, Z, cmap=self.cm_bg, alpha=.8)
        self._ax.scatter(self.X[:, 0], self.X[:, 1], c=self.Y, cmap=self.cm_points)
        if self.X_test is not None:
            self._ax.scatter(self.X_test[:, 0], self.X_test[:, 1], c=self.Y_test, cmap=self.cm_points, alpha=0.3)
        self._present(self._fig)

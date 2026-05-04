import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output
from matplotlib.colors import ListedColormap

from livelossplot.outputs.base_output import OutputMode


class BaseSubplot:
    def __init__(self):
        self.output_mode: OutputMode = 'notebook'

    def draw(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        self.draw(*args, **kwargs)

    def set_output_mode(self, mode: OutputMode) -> None:
        self.output_mode = mode

    def _present(self, fig: plt.Figure) -> None:
        if self.output_mode == 'notebook':
            clear_output(wait=True)
            plt.show()
        else:
            plt.draw()
            plt.pause(0.05)


class Plot1D(BaseSubplot):
    def __init__(self, model, X, Y):
        super().__init__()
        self.model = model
        self.X = X
        self.Y = Y

    def predict(self, model, X):
        return model.predict(X)

    def draw(self, *args, **kwargs):
        plt.plot(self.X, self.Y, 'r.', label="Ground truth")
        plt.plot(self.X, self.predict(self.model, self.X), '-', label="Model")
        plt.title("Prediction")
        plt.legend(loc='lower right')


class Plot2d(BaseSubplot):
    def __init__(self, model, X, Y, validation_data=(None, None), h=0.02, margin=0.25):
        super().__init__()

        self.model = model
        self.X = X
        self.Y = Y
        self.X_test, self.Y_test = validation_data

        self.cm_bg = plt.cm.RdBu
        self.cm_points = ListedColormap(['#FF0000', '#0000FF'])

        x_min = X[:, 0].min() - margin
        x_max = X[:, 0].max() + margin
        y_min = X[:, 1].min() - margin
        y_max = X[:, 1].max() + margin
        self.xx, self.yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        self._fig: plt.Figure | None = None
        self._ax: plt.Axes | None = None

    def predict(self, model, X):
        return model.predict(X)

    def send(self, logger):
        if self._fig is None or not plt.fignum_exists(self._fig.number):
            self._fig, self._ax = plt.subplots()
        else:
            self._ax.clear()

        Z = self.predict(self.model, np.c_[self.xx.ravel(), self.yy.ravel()])[:, 1]
        Z = Z.reshape(self.xx.shape)
        self._ax.contourf(self.xx, self.yy, Z, cmap=self.cm_bg, alpha=0.8)
        self._ax.scatter(self.X[:, 0], self.X[:, 1], c=self.Y, cmap=self.cm_points)
        if self.X_test is not None:
            self._ax.scatter(self.X_test[:, 0], self.X_test[:, 1], c=self.Y_test, cmap=self.cm_points, alpha=0.3)
        self._present(self._fig)

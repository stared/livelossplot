# livelossplot

[![livelossplot version - PyPI](https://img.shields.io/pypi/v/livelossplot)](https://pypi.org/project/livelossplot/)
![PyPI status](https://img.shields.io/pypi/status/livelossplot.svg)
![MIT license - PyPI](https://img.shields.io/pypi/l/livelossplot.svg)
![Python version - PyPI](https://img.shields.io/pypi/pyversions/livelossplot.svg)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/stared/livelossplot/Python%20package)](https://github.com/stared/livelossplot/actions)
[![Downloads](http://pepy.tech/badge/livelossplot)](http://pepy.tech/count/livelossplot)
[![Twitter @pmigdal](https://img.shields.io/twitter/follow/pmigdal)](https://twitter.com/pmigdal)

Don't train deep learning models blindfolded! Be impatient and look at each epoch of your training!

([RECENT CHANGES](CHANGELOG.md), [EXAMPLES IN COLAB](https://colab.research.google.com/github/stared/livelossplot), [API LOOKUP](http://p.migdal.pl/livelossplot/), [CODE](https://github.com/stared/livelossplot))

A live training loss plot in [Jupyter Notebook](http://jupyter.org/) for [Keras](https://keras.io/), [PyTorch](http://pytorch.org/) and other frameworks. An open-source Python package by [Piotr Migdał](https://p.migdal.pl/), [Bartłomiej Olechno](https://github.com/Bartolo1024/) and [others](https://github.com/stared/livelossplot/graphs/contributors). **Open for collaboration!** (Some tasks are as simple as writing code docstrings, so - no excuses! :))

```python
from livelossplot import PlotLossesKeras

model.fit(X_train, Y_train,
          epochs=10,
          validation_data=(X_test, Y_test),
          callbacks=[PlotLossesKeras()],
          verbose=0)
```

![Animated fig for livelossplot tracking log-loss and accuracy](https://raw.githubusercontent.com/stared/livelossplot/master/livelossplot.gif)

- (The most FA)Q: Why not TensorBoard?
- A: Jupyter Notebook compatibility (for exploration and teaching). The simplicity of use.

## Installation

To install [this version from PyPI](https://pypi.org/project/livelossplot/), type:

```bash
pip install livelossplot
```

To get the newest one from this repo (note that we are in the alpha stage, so there may be frequent updates), type:

```bash
pip install git+git://github.com/stared/livelossplot.git
```

## Examples

Look at notebook files with full working [examples](https://github.com/stared/livelossplot/blob/master/examples/):

- [keras.ipynb](https://github.com/stared/livelossplot/blob/master/examples/keras.ipynb) - a Keras callback
- [minimal.ipynb](https://github.com/stared/livelossplot/blob/master/examples/minimal.ipynb) - a bare API, to use anywhere
- [bokeh.ipynb](https://github.com/stared/livelossplot/blob/master/examples/bokeh.ipynb) - a bare API, plots with Bokeh ([open it in Colab to see the plots](https://colab.research.google.com/github/stared/livelossplot/blob/master/examples/bokeh.ipynb))
- [pytorch.ipynb](https://github.com/stared/livelossplot/blob/master/examples/pytorch.ipynb) - a bare API, as applied to PyTorch
- [2d_prediction_maps.ipynb](https://github.com/stared/livelossplot/blob/master/examples/2d_prediction_maps.ipynb) - example of custom plots - 2d prediction maps (0.4.1+)
- [poutyne.ipynb](https://github.com/stared/livelossplot/blob/master/examples/poutyne.ipynb) - a Poutyne callback ([Poutyne](https://poutyne.org/) is a Keras-like framework for PyTorch)
- [torchbearer.ipynb](https://github.com/stared/livelossplot/blob/master/examples/torchbearer.ipynb) - an example using the built in functionality from torchbearer ([torchbearer](https://github.com/ecs-vlc/torchbearer) is a model fitting library for PyTorch)
- [neptune.py](https://github.com/stared/livelossplot/blob/master/examples/neptune.py) and [neptune.ipynb](https://github.com/stared/livelossplot/blob/master/examples/neptune.ipynb) - a [Neptune.AI](https://neptune.ai/)
- [matplotlib.ipynb](https://github.com/stared/livelossplot/blob/master/examples/matplotlib.ipynb) - a Matplotlib output example
- [various_options.ipynb](https://github.com/stared/livelossplot/blob/master/examples/various_options.ipynb) - an extended API for metrics grouping and custom outputs

You [run examples in Colab](https://colab.research.google.com/github/stared/livelossplot).

## Overview

Text logs are easy, but it's easy to miss the most crucial information: is it learning, doing nothing or overfitting?
Visual feedback allows us to keep track of the training process. Now there is one for Jupyter.

If you want to get serious - use [TensorBoard](https://www.tensorflow.org/programmers_guide/summaries_and_tensorboard), .
But what if you just want to train a small model in Jupyter Notebook? Here is a way to do so, using `livelossplot` as a plug&play component

### from livelossplot import ...

`PlotLosses` for a generic API.

```{python}
plotlosses = PlotLosses()
plotlosses.update({'acc': 0.7, 'val_acc': 0.4, 'loss': 0.9, 'val_loss': 1.1})
plot.send()  # draw, update logs, etc
```

There are callbacks for common libraries and frameworks: `PlotLossesKeras`, `PlotLossesKerasTF`, `PlotLossesPoutyne`, `PlotLossesIgnite`.

Feel invited to write, and contribute, your adapter.
If you want to use a bare logger, there is `MainLogger`.

### from livelossplot.outputs import ...

Plots: `MatplotlibPlot`, `BokehPlot`.

Loggers: `ExtremaPrinter` (to standard output), `TensorboardLogger`, `TensorboardTFLogger`, `NeptuneLogger`.

To use them, initialize PlotLosses with some outputs:

```{python}
plotlosses = PlotLosses(outputs=[MatplotlibPlot(), TensorboardLogger()])
```

There are custom `matplotlib` plots in `livelossplot.outputs.matplotlib_subplots` you can pass in `MatplotlibPlot` arguments.

If you like to plot with [Bokeh](https://docs.bokeh.org/en/latest/) instead of [matplotlib](https://matplotlib.org/), use

```{python}
plotlosses = PlotLosses(outputs=[BokehPlot()])
```

## Sponsors

This project supported by [Jacek Migdał](http://jacek.migdal.pl/), [Marek Cichy](https://medium.com/@marekkcichy/). [Join the sponsors - show your ❤️ and support, and appear on the list](https://github.com/sponsors/stared)! It will give me time and energy to work on this project.

This project is also supported by a European program *Program Operacyjny Inteligentny Rozwój* for [GearShift - building the engine of behavior of wheeled motor vehicles and map’s generation based on artificial intelligence algorithms implemented on the Unreal Engine platform](https://mapadotacji.gov.pl/projekty/874596/?lang=en) lead by ECC Games (NCBR grant GameINN).

## Trivia

It started as [this gist](https://gist.github.com/stared/dfb4dfaf6d9a8501cd1cc8b8cb806d2e). Since it went popular, I decided to rewrite it as a package.

Oh, and I am in general interested in data vis, see [Simple diagrams of convoluted neural networks](https://medium.com/inbrowserai/simple-diagrams-of-convoluted-neural-networks-39c097d2925b) (and overview of deep learning architecture diagrams):

> A good diagram is worth a thousand equations — let’s create more of these!

...or [my other data vis projects](https://p.migdal.pl/projects/).

## Todo

If you want more functionality - open an [Issue](https://github.com/stared/livelossplot/issues) or even better - prepare a [Pull Request](https://github.com/stared/livelossplot/pulls).

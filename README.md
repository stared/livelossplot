# livelossplot

![PyPI version](https://img.shields.io/pypi/pyversions/livelossplot.svg)
![PyPI license](https://img.shields.io/pypi/l/livelossplot.svg)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/stared/livelossplot/Python package)](https://github.com/stared/livelossplot/actions)
![PyPI status](https://img.shields.io/pypi/status/livelossplot.svg)
[![Downloads](http://pepy.tech/badge/livelossplot)](http://pepy.tech/count/livelossplot)
[![Twitter @pmigdal](https://img.shields.io/twitter/follow/pmigdal)](https://twitter.com/pmigdal)

Don't train deep learning models blindfolded! Be impatient and look at each epoch of your training!

**🎉 New release 0.5.0 (20 Mar 2020). See [CHANGELOG](CHANGELOG.md) and updated [EXAMPLES IN COLAB](https://colab.research.google.com/github/stared/livelossplot). There are some API changes, to make it better, cleaner, and more modular. 🎉**

A live training loss plot in [Jupyter Notebook](http://jupyter.org/) for [Keras](https://keras.io/), [PyTorch](http://pytorch.org/) and other frameworks. An open-source Python package by [Piotr Migdał](https://p.migdal.pl/), [Bartłomiej Olechno](https://github.com/Bartolo1024/) and [others](https://github.com/stared/livelossplot/graphs/contributors). **Open for collaboration!** (Some tasks are as simple as writing code docstrings, so - no excuses! :))

This project supported by [Jacek Migdał](http://jacek.migdal.pl/), [Marek Cichy](https://medium.com/@marekkcichy/). [Join the sponsors - show your ❤️ and support, and appear on the list](https://github.com/sponsors/stared)! It will give me time and energy to work on this project.


```
from livelossplot import PlotLossesKeras

model.fit(X_train, Y_train,
          epochs=10,
          validation_data=(X_test, Y_test),
          callbacks=[PlotLossesKeras()],
          verbose=0)
```

![](livelossplot.gif)

So remember, [log your loss](https://twitter.com/pmigdal/status/943764924983017473)!

* (The most FA)Q: Why not TensorBoard?
* A: Jupyter Notebook compatibility (for exploration and teaching). The simplicity of use.

## Installation

To install [this version from PyPI](https://pypi.org/project/livelossplot/), type:

```
pip install livelossplot
```

To get the newest one from this repo (note that we are in the alpha stage, so there may be frequent updates), type:

```
pip install git+git://github.com/stared/livelossplot.git
```

## Examples

Look at notebook files with full working [examples](https://github.com/stared/livelossplot/blob/master/examples/):

* [keras.ipynb](https://github.com/stared/livelossplot/blob/master/examples/keras.ipynb) - a Keras callback
* [minimal.ipynb](https://github.com/stared/livelossplot/blob/master/examples/minimal.ipynb) - a bare API, to use anywhere
* [pytorch.ipynb](https://github.com/stared/livelossplot/blob/master/examples/pytorch.ipynb) - a bare API, as applied to PyTorch
* [2d_prediction_maps.ipynb](https://github.com/stared/livelossplot/blob/master/examples/2d_prediction_maps.ipynb) - example of custom plots - 2d prediction maps (0.4.1+)
* [poutyne.ipynb](https://github.com/stared/livelossplot/blob/master/examples/poutyne.ipynb) - a Poutyne callback ([Poutyne](https://poutyne.org/) is a Keras-like framework for PyTorch)
* [torchbearer.ipynb](https://github.com/stared/livelossplot/blob/master/examples/torchbearer.ipynb) - an example using the built in functionality from torchbearer ([torchbearer](https://github.com/ecs-vlc/torchbearer) is a model fitting library for PyTorch)
* [neptune.py](https://github.com/stared/livelossplot/blob/master/examples/neptune.py)  and [neptune.ipynb](https://github.com/stared/livelossplot/blob/master/examples/neptune.ipynb) - a [Neptune.AI](https://neptune.au/)

## Overview

Text logs are easy, but it's easy to miss the most crucial information: is it learning, doing nothing or overfitting?

Visual feedback allows us to keep track of the training process. Now there is one for Jupyter.

If you want to get serious - use [TensorBoard](https://www.tensorflow.org/programmers_guide/summaries_and_tensorboard). See `livelossplot.outputs` for loggers, plots and any other outputs.

But what if you just want to train a small model in Jupyter Notebook? Here is a way to do so, using `livelossplot` as a plug&play component.

It started as [this gist](https://gist.github.com/stared/dfb4dfaf6d9a8501cd1cc8b8cb806d2e). Since it went popular, I decided to rewrite it as a package.

Oh, and I am in general interested in data vis, see [Simple diagrams of convoluted neural networks](https://medium.com/inbrowserai/simple-diagrams-of-convoluted-neural-networks-39c097d2925b) (and overview of deep learning architecture diagrams):

> A good diagram is worth a thousand equations — let’s create more of these!

...or [my other data vis projects](https://p.migdal.pl/projects/).

## Todo

If you want more functionality - open an [Issue](https://github.com/stared/livelossplot/issues) or even better - prepare a [Pull Request](https://github.com/stared/livelossplot/pulls).

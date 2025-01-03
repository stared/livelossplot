# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.6] - 2025-01-03

### Fixed

- MatplotlibPlot now works in script mode - [a long awaited feature](https://github.com/stared/livelossplot/issues/2)!
- GitHub Actions using current Python versions.

### Added

- `PlotLosses(figsize=(10, 10))` to set the size of the figure due to [popular demand](https://github.com/stared/livelossplot/issues/139).
- Script vs notebook mode detection.

## [0.5.5] - 2022-04-03

## Fixed

- Support for Python 3.7 (see [this PR](https://github.com/stared/livelossplot/pull/136))

## Added

- Support for Python 3.10 (see [this PR](https://github.com/stared/livelossplot/pull/136))

## [0.5.4] - 2021-02-03

## Added

- `from_step` option to display epochs from a given one (e.g. `from_step=2`) or only last epochs (e.g. `from_step=-10`), [see this request](https://github.com/stared/livelossplot/issues/124).
- Tests for Python 3.9.

## Dropped

- Support for Python 3.5.

## [0.5.3] - 2020-07-24

## Added

- API to add outputs with strings `PlotLosses(outputs=['MatplotlibPlot', 'TensorboardLogger'])`, in case of default parameters.
- API to add outputs with chaining `PlotLosses(outputs=[]).to_matplotlib(**kwargs1).to_tensorboard(**kwargs2)`.
- README in pdoc3 documentation.

## Fixed

- An error introduced in `0.5.2` with empty subplots (i.e. if the total number of subplots is not divisible the number of columns).

## Changed

- `MatplotlibPlot._default_after_plots` contains `plt.show()` and`fig.savefig(...)`, so that display and save options can be altered with `MatplotlibPlot(after_plots=....)`.

## [0.5.2] - 2020-07-19

### Added

- Auto-generated documentation with [pdoc3](https://pypi.org/project/pdoc3/): <http://p.migdal.pl/livelossplot/>.
- Option to generate custom matplotlib plot options (e.g. log scale, no legend, etc) with `MatplotlibPlot(after_subplot=...)` and general for display `MatplotlibPlot(after_subplot=..., after_plots=....)`.

### Changed

- Docstrings to Google-style (see [https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format](https://stackoverflow.com/questions/3898572/what-is-the-standard-python-docstring-format)).
- Using object-oriented matplotlib API for plots (`ax.` not `plt.`), vide [this issue](https://github.com/stared/livelossplot/issues/16).

## [0.5.1] - 2020-05-28

### Added

- Bokeh colors, scaling, and hover tooltip (see [this PR for screenshots](https://github.com/stared/livelossplot/pull/106)).
- Tests for Neptune, better tests in general.
- Nice Issue templates.

### Fixed

- Bokeh example.
- Made it working in general.

## [0.5.0] - 2020-03-20

It is a major rewrite, with breaking API changes.
It requires Python 3.5+, and ideally 3.6+.

**Work in progress - expect fixes and additions in `0.5.*`.**

### Added

- Docstrings.
- Tests (using `pytest`).
- Continuous integration (using GitHub Actions).
- Type hints, mostly for better development and more explicit documentation.
- Way to write new output plugins (see `outputs` directory).
- Examples are readily runnable on Colab.
- A more general way generate groups for plots based on Regex patterns.
- Bokeh plot - an initial version.

### Refactored

- A major refactor of the whole structure.
- `PlotLosses` is no longer a god object.
- Organized input plugins in the `inputs` directory.

### Fixed

- Updated `neptune` and `tensorboard` plugins to support current APIs of the respective libraries.

### Removed

- Python 2.7 support.
- Python 3.4 support - due to type hints.
- Python 3.5 support priority. Right it installs an older version of `matplotlib`, 3.0 (the last working with Python 3.5). The current version of `matplotlib` is 3.2, see https://matplotlib.org/3.2.0/users/installing.html. Support for Python 3.5 for `livelossplot` may be dropped at any moment.

## [0.4.2] - 2020-03-06

### Added

- PyTorch Ignite plugin and example.
- GitHub sponsor option.

### Fixed

- Tensorboard path for Windows.
- Changed PyToune to Poutyne to reflect the API name change of the respective library.

## [0.4.1] - 2019-05-26

### Added

- Custom `matplotlib` subplots.
- 2d plot prediction.

## [0.4.0] - 2019-05-06

For now, it is prehistory.

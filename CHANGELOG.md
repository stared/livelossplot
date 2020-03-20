# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
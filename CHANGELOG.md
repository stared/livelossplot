# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - unreleased

It is a major rewrite, with breaking API changes.

**Work in progress - expect more changes soon.**

### Added

- Docstrings.
- Tests (using pytest).
- Continuous integration (using GitHub Actions).
- Type hints (so it works for Python 3.5+).
- Way to write new output plugins (see `output_plugins` directory).
- Examples are readily runable on Colab. 

### Refactored

- A major refactor of the whole structure.
- `PlotLosses` is not longer a god object.
- Organized input plugins in `input_plugins` directory.


### Fixed

- Updated `neptune` and `tensorboard` plugins to support current APIs od the respective libraries.

### Removed

- Python 2.7 support. 


## [0.4.2] - 2020-03-06

### Added

- PyTorch Ignite plugin and example.
- GitHub sponsor option.

### Fixed

- Tensorboard path for Windows.
- Changed PyToune to Poutyne to reflect API name change of the respective library.


## [0.4.1] - 2019-05-26

### Added

- Custom matplotlib subplots.
- 2d plot prediction.


## [0.4.0] - 2019-05-06

For now it is prehistory. 
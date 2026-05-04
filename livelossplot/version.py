"""Livelossplot version number.

The version is defined in pyproject.toml and read here from the installed
package metadata, so there is a single source of truth.
"""

from importlib.metadata import version

__version__ = version("livelossplot")

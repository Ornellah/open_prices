"""
OpenPrices is a package for processing and analyzing data.

This package provides functions for data processing and analysis and
exposes the data paths defined in the config module.

Main features
-------------
1. Three functions for data processing and analysis
2. Exposes data paths defined in the config module

Configuration
-------------
The package directly exposes the necessary functions and paths
so that other modules or users can use them
without importing the configuration module separately.
"""

from open_prices import config  # noqa: F401

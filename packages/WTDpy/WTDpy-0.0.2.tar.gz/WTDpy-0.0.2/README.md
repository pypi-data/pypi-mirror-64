[![CircleCI](https://circleci.com/gh/uijl/wtdpy.svg?style=svg)](https://circleci.com/gh/uijl/wtdpy)
[![Documentation Status](https://readthedocs.org/projects/wtdpy/badge/?version=latest)](https://wtdpy.readthedocs.io/en/latest/?badge=latest)
[![PyPI Latest Release](https://img.shields.io/pypi/v/wtdpy.svg)](https://pypi.org/project/wtdpy/)

# WTDpy

Basic calls to the World Trading Data API with Python. 
You can find the documentation over [here](https://wtdpy.readthedocs.io).

## Starting up

The code snip below shows how you can initialise the WTDpy class. As soon as you have the `WTDpy` class initialised you can start calling the various functions.

```python
# Import wtdpy library
from wtdpy import WTDpy

# Specifiy your api key
api_token = "Your_API_Token"

# Initialise class
wtdpy = WTDpy(api_token=api_token)

# Search for a stock or index
MSFT = wtdpy.search("Microsoft")
```

## Installation

To install WTDpy, run this command in your terminal:

``` bash
# Use pip to install wtdpy
pip install wtdpy
```

This is the preferred method to install WTDpy, as it will always install the most recent stable release. If you do not have
[pip](https://pip.pypa.io) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) 
can guide you through the process.

Downloading and installing WTDpy from source is also possible, follow the code below.

``` bash
# Download the package
git clone https://github.com/uijl/wtdpy

# Go to the correct folder
cd wtdpy

# Install package
pip install -e .
```

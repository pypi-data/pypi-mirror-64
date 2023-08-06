========
Examples
========

This small example guide will cover the basic start-up and the functions now available in WTDpy:

- Import package and set-up a class.
- Make a call to the World Trading Data API.


Start-Up
--------

The first part is importing the package and setting up the class with your own API key.

.. code:: python3

    # Import wtdpy
    from wtdpy import WTDpy

If you do not yet have your own API key of the World Trading Data API you can create a free `account`_. 
With this free account you can request up to 250 historical time series per day. As soon as you log on to your dashboard it shows
large on the screen "Your API Token". Copy this random string and assign it to a variable.

.. code:: python3

    # Set your own api_key
    api_key = "your_unique_api_key"

    # Create the class
    wtd = WTDpy(api_token = api_key)


Make a call to the API
----------------------

Once you have initialised your WTDpy class you can make a call to the World Trading data API.
If you are not sure about the symbol you want to look up you can check if the symbol you want is returned by the API with the following code.

.. code:: python3

    # Check for correct response
    # Returns True if the returned symbol is equal to the request
    symbol = ["^AEX"]
    wtd.search_available_data(symbol = symbol)

If you have selected the correct symbol, or list of symbols, you can use the code below to request all the available historical data.

.. code:: python3

    # Request historical time series of two indices
    symbol = ["^AEX", "^DAX"]
    wtd.get_historical_data(symbol = symbol)


.. _account: https://www.worldtradingdata.com/
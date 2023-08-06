"""Testing get requests for historical data."""

from datetime import datetime

import pandas as pd
import pytest


@pytest.mark.parametrize("symbol", [["^AEX"], ["^AEX", "^DAX"]])
def test_historical_data(symbol, wtdpy):
    """Test historical data request without additional data."""

    response = wtdpy.get_historical_data(symbol)

    # Check if correct symbols are returned
    for ix, key in enumerate(response.keys()):
        assert key == symbol[ix]


@pytest.mark.parametrize("symbol", [["^AEX"], ["^AEX", "^DAX"]])
def test_historical_data_date_from(symbol, wtdpy):
    """Test historical data request with a timewindow."""

    # Correct string
    date_from = "2020-01-02"
    response = wtdpy.get_historical_data(symbol, date_from=date_from)

    for _, key in enumerate(response.keys()):
        assert next(iter(response[key]["history"])) == "2020-01-02"

    # DateTime object
    date_from = datetime(2020, 1, 2)
    response = wtdpy.get_historical_data(symbol, date_from=date_from)

    for _, key in enumerate(response.keys()):
        assert next(iter(response[key]["history"])) == "2020-01-02"

    # Incorrect string
    date_from = "01-01-2020"

    with pytest.raises(TypeError):
        response = wtdpy.get_historical_data(symbol, date_from=date_from)


@pytest.mark.parametrize("symbol", [["^AEX"], ["^AEX", "^DAX"]])
def test_historical_data_date_to(symbol, wtdpy):
    """Test historical data request with a timewindow."""

    # Correct string
    date_to = "2020-02-01"
    response = wtdpy.get_historical_data(symbol, date_to=date_to)

    for _, key in enumerate(response.keys()):
        assert list(response[key]["history"].keys())[-1] == "2020-01-31"

    # DateTime object
    date_to = datetime(2020, 2, 1)
    response = wtdpy.get_historical_data(symbol, date_to=date_to)

    for _, key in enumerate(response.keys()):
        assert list(response[key]["history"].keys())[-1] == "2020-01-31"

    # Incorrect string
    date_to = "01-02-2020"

    with pytest.raises(TypeError):
        response = wtdpy.get_historical_data(symbol, date_to=date_to)


@pytest.mark.parametrize("symbol", [["^AEX"], ["^AEX", "^DAX"]])
def test_historical_data_sort(symbol, wtdpy):
    """Test historical data request with a sort parameter."""

    # Basic request (ascending)
    response_asc = wtdpy.get_historical_data(symbol)

    # Descending
    response_desc = wtdpy.get_historical_data(symbol, sort="desc")

    for _, key in enumerate(response_asc.keys()):
        assert (
            list(response_asc[key]["history"].keys())[0]
            == list(response_desc[key]["history"].keys())[-1]
        )
        assert (
            list(response_asc[key]["history"].keys())[-1]
            == list(response_desc[key]["history"].keys())[0]
        )


@pytest.mark.parametrize("symbol", [["^AEX"], ["^AEX", "^DAX"]])
def test_historical_data_output(symbol, wtdpy):
    """Test historical data request with an output parameter."""

    # Pandas DataFrame
    response = wtdpy.get_historical_data(symbol, output="df")

    if len(symbol) == 1:
        assert type(response) == pd.DataFrame

    else:
        for _, key in enumerate(response.keys()):
            assert type(response[key]) == pd.DataFrame


@pytest.mark.parametrize("symbol", [["test_1"], ["test_1", "test_2"]])
def test_historical_data_output_false_symbol(symbol, wtdpy):
    """Test historical data request with a false symbol."""

    with pytest.raises(ValueError):
        wtdpy.get_historical_data(symbol)

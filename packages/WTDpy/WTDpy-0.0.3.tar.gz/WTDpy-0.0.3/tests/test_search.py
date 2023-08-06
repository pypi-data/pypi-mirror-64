"""Testing get requests for overall search."""

import pytest


@pytest.mark.parametrize(
    "symbol", [["Apple Computers"], ["Apple Computers", "Microsoft"]]
)
def test_search(symbol, wtdpy):
    """Test search request without additional data."""

    # Symbols are correct so should return `True`
    response = wtdpy.search(symbol)
    assert len(symbol) == len(response)

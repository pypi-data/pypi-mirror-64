import json
from datetime import datetime
from typing import List, Sequence, Union

import httpx
import pandas as pd


class WTDpy:
    """ Python wrapper for the World Trading Data API.

    **Parameters**
    
    api_token : str 
        Your personal API token from https://www.worldtradingdata.com/.
    
    **Attributes**

    api_token : str 
        Your personal API token from https://www.worldtradingdata.com/.
    
    url : str
        The base url for requesting the API.

    **Notes**

    Create an account on https://www.worldtradingdata.com/ 
    to obtain your API key. It will show on the top of your
    personal dashboard. You can make 250 API calls per day
    with the free tier.

    Currently supporting:
        * Historical data;
        * Checking if a symbol excists.

    """

    def __init__(self, api_token: str) -> None:
        """Initialisation."""

        self.url = "https://api.worldtradingdata.com/api/v1/"
        self.api_token = api_token

    # TODO: error if connection if request is failing

    def get_historical_data(
        self,
        symbol: Union[str, Sequence[str]],
        date_from: Union[datetime, str] = None,
        date_to: Union[datetime, str] = None,
        sort: str = "asc",
        output: str = "dict",
    ) -> Union[dict, pd.DataFrame]:
        """ Get the historical data for the given symbol.

        **Parameters**
        
        symbol : str or list of str
            A string or list of strings such as "^AEX", 
            or ["^AEX", "^DAX"]. The symbols should match 
            the format as shown on the World Trading Data site. 
            You can check https://www.worldtradingdata.com/search 
            to see what data is available at World Trading Data.
        
        date_from : str or datetime
            A string representing a date in isoformat (yyyy-mm-dd), 
            a datetime object or None. If no data is provided 
            the earliest date will be requested.

        date_to: str or datetime
            A string representing a date in isoformat (yyyy-mm-dd), 
            a datetime object or None. If no data is provided 
            the latest date will be requested.

        sort: str
            A string representing the sorting of the requested
            data. Either ascending "asc" or descending "desc".

        output: str
            A string representing the desired output. Either
            `dict` for a python dict or "df" for a pandas DataFrame.
        
        **Raises**
        
        ValueError
            * If provided symbol is not available.

        TypeError
            * If `date_from` is not a correct string or datetime object
            * If `date_to` is not a correct string or datetime object
            * If `sort` is not a correct string
            * If `output` is not a correct string

        **Returns**
        
        to_return : dict or pd.DataFrame
            A dictionary or a pandas DataFrame. If `symbol` is a list
            then a dictionary of pandas DataFrames will be returned.

        """

        request_url = self.url + "history"
        params = {"api_token": self.api_token}

        # Check date from
        if type(date_from) == str:
            try:
                datetime.strptime(date_from, "%Y-%m-%d")
            except:
                raise TypeError(
                    f"Provided date_from '{date_from}' does not match isoformat yyyy-mm-dd"
                )
            params.update({"date_from": date_from})
        elif type(date_from) == datetime:
            params.update({"date_from": str(date_from.date())})

        # Check date to
        if type(date_to) == str:
            try:
                datetime.strptime(date_to, "%Y-%m-%d")
            except:
                raise TypeError(
                    f"Provided date_to '{date_to}' does not match isoformat yyyy-mm-dd"
                )
            params.update({"date_to": date_to})
        elif type(date_to) == datetime:
            params.update({"date_to": str(date_to.date())})

        # Check sorting request
        if not sort in ["asc", "desc"]:
            raise TypeError(
                f"Provided sort '{sort}' is not equal to either 'asc' or 'desc'"
            )
        else:
            params.update({"sort": sort})

        # Check requested output
        if not output in ["dict", "df"]:
            raise TypeError(
                f"Provided output '{output}' is not equal to either 'dict' or 'df'"
            )

        # Prepare request per symbol
        if type(symbol) == str:
            symbol = [symbol]

        # Returning dict
        to_return = {}

        for sym in symbol:

            # Check if provided symbol are available
            if self.search_available_data(sym):
                params.update({"symbol": sym})
            else:
                raise ValueError("Requested symbols are not available")

            # Make the request
            response = httpx.get(request_url, params=params)
            response = response.json()

            # Alter the response based on input
            if output == "dict":
                to_return.update({sym: response})

            elif output == "df":
                to_return.update(
                    {sym: pd.DataFrame.from_dict(response["history"], orient="index")}
                )

        if len(to_return) == 1 and output == "df":
            return to_return[sym]

        else:
            return to_return

    def search_available_data(
        self,
        symbol: Union[str, Sequence[str]],
        list_alternatives: bool = False,
        number_of_alternatives: int = 1,
    ) -> Union[bool, Sequence[dict]]:
        """ Check if the requested data is available.

        **Parameters**
        
        symbol : str or list of str
            A string or list of strings such as "^AEX", 
            or ["^AEX", "^DAX"]. The symbols should match 
            the format as shown on the World Trading Data site. 
            You can check https://www.worldtradingdata.com/search 
            to see what data is available at World Trading Data.
        
        list_alternatives : bool
            If `True` a list of likely matches is presented 
        
        number_of_alternatives : int
            The number of alternatives, besides the top hit, 
            that are checked whether or not they match the 
            provided symbol. 

        **Returns**
        
        response : bool or list
            A boolean to check whether data is avaible. If 
            `list_alternatives` is `True` and a symbol is not found
            a list with possible alternatives will be returned.

        """

        request_url = self.url + "stock_search"
        params = {"api_token": self.api_token, "limit": number_of_alternatives}

        # Matching symbols found
        matching_symbols = False

        # possible alternatives
        if list_alternatives:
            alternatives = []

        # Prepare request per symbol
        if type(symbol) == str:
            symbol = [symbol]

        for sym in symbol:
            symbol_found = False
            params.update({"search_term": sym})
            response = httpx.get(request_url, params=params)
            response = response.json()

            for ix, _ in enumerate(response["data"]):
                if response["data"][ix]["symbol"] == sym:
                    symbol_found = True
                    break

                else:
                    symbol_found = False

                    if list_alternatives:
                        alternatives.append(
                            {
                                "Symbol": response["data"][ix]["symbol"],
                                "Name": response["data"][ix]["name"],
                            }
                        )

            if symbol_found:
                matching_symbols = True

        # Return either a bool or a list with alternative symbols
        if not list_alternatives:
            return matching_symbols
        elif not alternatives:
            return matching_symbols
        else:
            return alternatives

    def search(
        self, query: Union[str, Sequence[str]], number_of_hits: int = 5
    ) -> Union[dict, Sequence[dict]]:
        """ Search the query in the World Trading Data database.

        **Parameters**
        
        query : str or list of str
            A string or list of strings such as "Apple computers"
            or ["Apple computers", "Microsoft"]. This is similar
            to manually checking https://www.worldtradingdata.com/search 
            to see what data is available at World Trading Data.
        
        number_of_hits : int
            The number of hits that will be returned. 

        **Returns**
        
        response : dict or list
            A dict, or a list of dicts, with the listed hits based on
            your search query.

        """

        request_url = self.url + "stock_search"
        params = {"api_token": self.api_token, "limit": number_of_hits}

        returned_hits = {}

        # Prepare request per symbol
        if type(query) == str:
            query = [query]

        for q in query:
            params.update({"search_term": q})
            returned_hits.update({q: []})

            response = httpx.get(request_url, params=params)
            response = response.json()

            for ix, _ in enumerate(response["data"]):
                returned_hits[q].append(
                    {
                        "Symbol": response["data"][ix]["symbol"],
                        "Name": response["data"][ix]["name"],
                    }
                )

        print(returned_hits)

        # Return the search results
        return returned_hits

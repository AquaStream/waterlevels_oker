import pandas as pd
import requests

from waterlevels_oker import utils
from waterlevels_oker.config import *


def get_climate_data():
    """
    Gets weather data from https://brightsky.dev/docs/#/operations/getWeather starting 2010-01-01 until now.
    """
    params = {
        "date": "2010-01-01",
        "dwd_station_id": "00662",
        "last_date": "2024-08-01",
    }

    url = "https://api.brightsky.dev/weather"
    response = requests.get(url, params=params)

    climate_data = pd.DataFrame(response.json()["weather"])
    climate_data.to_csv(utils.get_raw_path("climate_data.csv"), index=False)

    return climate_data


def get_forecast(start: str, end: str) -> pd.DataFrame:
    """
    Get weather forecaste from start to end date.

    Parameters
    ----------
    start : str
        Timestamp of first weather record (or forecast) to retrieve, in ISO 8601 format. May contain time and/or UTC offset.
        Examples:
        2023-08-07
        2023-08-07T08:00+02:00
    end : str
        Timestamp of last weather record (or forecast) to retrieve, in ISO 8601 format. Will default to date + 1 day.
        Examples:
        2023-08-08
        2023-08-07T23:00+02:00

    Returns
    -------
    pd.DataFrame
        Dataframe containing the weather forecast
    """
    params = {
        "date": start,
        "dwd_station_id": "00662",
        "last_date": end,
    }

    url = "https://api.brightsky.dev/weather"
    response = requests.get(url, params=params)

    forecast = pd.DataFrame(response.json()["weather"])

    return forecast

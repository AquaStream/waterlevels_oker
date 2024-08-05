import pandas as pd
import requests

from waterlevels_oker import utils
from waterlevels_oker.config import *


def get_raw_weather_data():
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


def preprocess_weather_data() -> pd.DataFrame:
    """
    Process raw weather data. Save as csv and return Dataframe.

    - Drops columns ["source_id",
        "condition",
        "precipitation_probability",
        "precipitation_probability_6h",
        "fallback_source_ids",
        "icon"]
    - Impute missing sunshine values during nighttime with 0

    Returns
    -------
    pd.DataFrame
        Preprocessed weather data
    """
    weather_raw = pd.read_csv(
        utils.get_raw_path("climate_data.csv"), parse_dates=[0], index_col=0
    )
    drop_cols = [
        "source_id",
        "condition",
        "precipitation_probability",
        "precipitation_probability_6h",
        "fallback_source_ids",
        "icon",
    ]
    weather_raw = weather_raw.drop(columns=drop_cols)
    # Impute missing sunshine values during nighttime with 0
    night_missing_sunshine = weather_raw.loc[
        weather_raw["sunshine"].isna()
        & weather_raw.index.hour.isin([21, 22, 23, 0, 1, 2])
    ].index
    weather_raw.loc[night_missing_sunshine, "sunshine"] = 0

    weather_raw = weather_raw.dropna(axis=0)

    weather_raw.to_csv(utils.get_processed_path("processed_weather.csv"))

    return weather_raw


def get_weather_data() -> pd.DataFrame:
    """
    Returns preprocessed weather data as Dataframe.

    Returns
    -------
    pd.DataFrame
        Processed weather data
    """
    weather_data = pd.read_csv(
        utils.get_processed_path("processed_weather.csv"), index_col=0
    )

    return weather_data
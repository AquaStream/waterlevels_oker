import pandas as pd
import requests
import numpy as np
from waterlevels_oker import utils
from waterlevels_oker.config import *


def get_climate_data():
    """
    Gets weather data from https://brightsky.dev/docs/#/operations/getWeather starting 2010-01-01 until now.
    """
    params = {
        "date": "2010-01-01",
        "dwd_station_id": "00662",
        "last_date": "2024-07-28",
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


def preprocess_ohrum_data() -> pd.DataFrame:
    """
    Process raw Ohrum data. Saves it as .csv and returns Dataframe

    Returns
    -------
    pd.DataFrame
        Processed Ohrum data
    """
    ohrum_data = pd.read_excel(utils.get_raw_path("Ohrum.xlsx"))
    ohrum_data = ohrum_data.dropna()

    ohrum_data = ohrum_data.rename(
        columns={"Waserstand relativ [cm]": "Waterlevel relative [cm]"}
    )

    # Create new datetime index
    ohrum_str = ohrum_data.astype("str")
    ohrum_data.index = pd.to_datetime(
        ohrum_str["Datum"] + " " + ohrum_str["Zeit"], format="%Y-%m-%d %H:%M:%S"
    )

    ohrum_data = ohrum_data.drop(columns=["Datum", "Zeit"])

    # Keep only measurements at full hour
    ohrum_data = ohrum_data.loc[ohrum_data.index.minute == 0]

    # Impute missing value at 2018-01-01 00:00 with mean
    ohrum_data.loc[ohrum_data["Waterlevel relative [cm]"] == " ---"] = np.mean(
        [ohrum_data.loc["2017-12-31 23:00:00"], ohrum_data.loc["2018-01-01 01:00:00"]]
    )
    ohrum_data = ohrum_data.astype(dtype={"Waterlevel relative [cm]": "float"})

    ohrum_data.to_csv(utils.get_processed_path("ohrum_data.csv"))

    return ohrum_data


def get_ohrum_data() -> pd.DataFrame:
    """
    Return processeed Ohrum data

    Returns
    -------
    pd.DataFrame
        Processed Ohrum data with DatatimeIndex and waterlevel measurements
    """
    ohrum_data = pd.read_csv(
        utils.get_processed_path("ohrum_data.csv"),
        index_col=0,
        parse_dates=[0],
        date_format="%Y-%m-%d %H:%M:%S",
    )

    return ohrum_data

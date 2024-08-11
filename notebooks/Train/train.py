# Commented out IPython magic to ensure Python compatibility.
from waterlevels_oker import utils
from waterlevels_oker.data import get_okertal_training_data, get_schladen_training_data, get_ohrum_training_data, get_bridge_training_data, get_eisenbuettel_training_data, get_wendenwehr_training_data
import pandas as pd
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import json

# %config InlineBackend.figure_format = "retina"

import pandas as pd
import requests
import numpy as np
from datetime import datetime
from datetime import timedelta
from waterlevels_oker import utils
from waterlevels_oker.config import *
import pickle


def get_raw_weather_data(city: str) -> pd.DataFrame:
    """
    Gets weather data from https://brightsky.dev/docs/#/operations/getWeather starting 2010-01-01 until 2024-07-31.

    Parameters
    ----------
    city : str
        City from
        ["okertal",
        "schladen",
        "ohrum",
        "schaeferbruecke",
        "eisenbuetteler_wehr",
        "wendenwehr"]

    Returns
    -------
    pd.Dataframe
        Raw weather data
    """
    cities = {
        "okertal": [51.85, 10.45],
        "schladen": [52.019, 10.54],
        "ohrum": [52.11, 10.56],
        "schaeferbruecke": [52.17, 10.51],
        "eisenbuetteler_wehr": [52.24, 10.52],
        "wendenwehr": [52.27, 10.52],
    }

    weather_raw = pd.DataFrame()
    for year in range(2012, 2025):
        params = {
            "date": "{}-01-01".format(year),
            "last_date": "{}-07-31".format(year + 1),
            "lat": cities[city][0],
            "lon": cities[city][1],
        }

        url = "https://api.brightsky.dev/weather"
        response = requests.get(url, params=params)
        weather = pd.DataFrame(response.json()["weather"])
        weather_raw = pd.concat([weather_raw, weather])

    return weather_raw


def get_forecast(city: str) -> pd.DataFrame:
    """
    Get weather forecaste from start to end date for the city specified.

    city : str
        City from
        ["okertal",
        "schladen",
        "ohrum",
        "schaeferbruecke",
        "eisenbuetteler_wehr",
        "wendenwehr"]

    Returns
    -------
    pd.DataFrame
        Dataframe containing the weather forecast
    """

    cities = {
        "okertal": [51.85, 10.45],
        "schladen": [52.019, 10.54],
        "ohrum": [52.11, 10.56],
        "schaeferbruecke": [52.17, 10.51],
        "eisenbuetteler_wehr": [52.24, 10.52],
        "wendenwehr": [52.27, 10.52],
    }

    start_date = datetime(2024, 8, 9)
    end_date = start_date + timedelta(days=7)

    params = {
        "date": start_date.isoformat(),
        "last_date": end_date.isoformat(),
        "lat": cities[city][0],
        "lon": cities[city][1],
    }

    url = "https://api.brightsky.dev/weather"
    response = requests.get(url, params=params)

    forecast = pd.DataFrame(response.json()["weather"])

    preprocessed = preprocess_weather_data(forecast)

    return preprocessed


def preprocess_weather_data(raw_data) -> pd.DataFrame:
    """
    Preprocesses raw weather data.

    Parameters
    ----------
    raw_data

    Returns
    -------
    pd.DataFrame
        Processed weather data
    """

    raw_data = raw_data.assign(
        timestamp=pd.to_datetime(raw_data["timestamp"])
    ).set_index("timestamp")

    # Drop timezone from datetime index
    raw_data.index = raw_data.index.tz_localize(None)

    drop_cols = [
        "source_id",
        "condition",
        "precipitation_probability",
        "precipitation_probability_6h",
        # "fallback_source_ids",
        "icon",
    ]
    raw_data = raw_data.drop(columns=drop_cols)
    if "fallback_source_ids" in raw_data.columns:
        raw_data = raw_data.drop(columns="fallback_source_ids")

    # Impute missing sunshine values during nighttime with 0
    night_missing_sunshine = raw_data.loc[
        raw_data["sunshine"].isna() & raw_data.index.hour.isin([21, 22, 23, 0, 1, 2])
    ].index
    raw_data.loc[night_missing_sunshine, "sunshine"] = 0

    raw_data = raw_data.bfill()

    daily_weather_data = raw_data.groupby(raw_data.index.date).mean()

    return daily_weather_data


def preprocess_okertal_data():
    okertal_data = pd.read_excel(utils.get_raw_path("Oker Daten.xlsx"), index_col=0)

    okertal_data = okertal_data.loc[:, ["Stauinhalt Okertalsperre [Mio.m³]"]].rename(
        columns={
            "Stauinhalt Okertalsperre [Mio.m³]": "fill_[mio.m³]",
        }
    )

    return okertal_data


def get_okertal_training_data():
    weather = get_raw_weather_data("okertal")

    processed_weather = preprocess_weather_data(weather)

    okertal_data = preprocess_okertal_data()

    full_data = processed_weather.join(okertal_data, how="inner").reset_index(
        names=["timestamp"]
    )
    return full_data


def get_schladen_training_data():
    weather = get_raw_weather_data("schladen")

    processed_weather = preprocess_weather_data(weather)

    okertal_data = preprocess_okertal_data()
    schladen_data = preprocess_brunswick_data().loc[:, "schladen"]

    full_data = (
        processed_weather.join(okertal_data, how="inner")
        .join(schladen_data, how="inner")
        .reset_index(names=["timestamp"])
    )
    return full_data


def get_ohrum_training_data():
    weather = get_raw_weather_data("ohrum")

    processed_weather = preprocess_weather_data(weather)

    schladen_data = preprocess_brunswick_data().loc[:, "schladen"]
    ohrum_data = preprocess_brunswick_data().loc[:, "ohrum_level"]

    full_data = (
        processed_weather.join(ohrum_data, how="inner")
        .join(schladen_data, how="inner")
        .reset_index(names=["timestamp"])
    )
    return full_data


def get_bridge_training_data():
    weather = get_raw_weather_data("schaeferbruecke")

    processed_weather = preprocess_weather_data(weather)

    ohrum_data = preprocess_brunswick_data().loc[:, "ohrum_level"]
    bridge_data = preprocess_brunswick_data().loc[:, "schaeferbridge"]

    full_data = (
        processed_weather.join(ohrum_data, how="inner")
        .join(bridge_data, how="inner")
        .reset_index(names=["timestamp"])
    )
    return full_data


def get_eisenbuettel_training_data():
    weather = get_raw_weather_data("eisenbuetteler_wehr")

    processed_weather = preprocess_weather_data(weather)

    bridge_data = preprocess_brunswick_data().loc[:, "schaeferbridge"]
    eisenbütteler_wehr_data = preprocess_brunswick_data().loc[:, "eisenbuetteler_wehr"]

    full_data = (
        processed_weather.join(bridge_data, how="inner")
        .join(eisenbütteler_wehr_data, how="inner")
        .reset_index(names=["timestamp"])
    )
    return full_data


def get_wendenwehr_training_data():
    weather = get_raw_weather_data("wendenwehr")

    processed_weather = preprocess_weather_data(weather)
    eisenbütteler_wehr_data = preprocess_brunswick_data().loc[:, "eisenbuetteler_wehr"]
    wendenwehr_data = preprocess_brunswick_data().loc[:, "wendenwehr"]

    full_data = (
        processed_weather.join(eisenbütteler_wehr_data, how="inner")
        .join(wendenwehr_data, how="inner")
        .reset_index(names=["timestamp"])
    )
    return full_data


def get_okertal_forecast_data():
    weather = get_forecast("okertal")

    processed_weather = preprocess_weather_data(weather)

    return processed_weather


def preprocess_brunswick_data() -> pd.DataFrame:
    measurements_2019 = pd.read_excel(
        utils.get_raw_path("Übersicht Pegelwerte 2019-2023.xlsx"),
        sheet_name="2019",
        header=[0, 1],
    )

    measurements_2019.columns = measurements_2019.columns.to_flat_index()
    measurements_2019 = measurements_2019.rename(
        columns={("Datum", "Unnamed: 1_level_1"): "timestamp"}
    )

    measurements_2020 = pd.read_excel(
        utils.get_raw_path("Übersicht Pegelwerte 2019-2023.xlsx"),
        sheet_name="2020",
        header=[0, 1],
    )

    measurements_2020.columns = measurements_2020.columns.to_flat_index()
    measurements_2020 = measurements_2020.rename(
        columns={("2020", "Unnamed: 1_level_1"): "timestamp"}
    )

    measurements_2021 = pd.read_excel(
        utils.get_raw_path("Übersicht Pegelwerte 2019-2023.xlsx"),
        sheet_name="2021",
        header=[1, 2],
    )

    measurements_2021.columns = measurements_2021.columns.to_flat_index()
    measurements_2021 = measurements_2021.rename(
        columns={("2021", "Unnamed: 1_level_1"): "timestamp"}
    )

    measurements_2022 = pd.read_excel(
        utils.get_raw_path("Übersicht Pegelwerte 2019-2023.xlsx"),
        sheet_name="2022",
        header=[0, 1],
    )

    measurements_2022.columns = measurements_2022.columns.to_flat_index()
    measurements_2022 = measurements_2022.rename(
        columns={(2022, "Uhrzeit.2"): "timestamp"}
    )

    measurements_2023 = pd.read_excel(
        utils.get_raw_path("Übersicht Pegelwerte 2019-2023.xlsx"),
        sheet_name="2023",
        header=[0, 1],
    )

    measurements_2023.columns = measurements_2023.columns.to_flat_index()
    measurements_2023 = measurements_2023.rename(
        columns={
            (2023, "Uhrzeit.2"): "timestamp",
        }
    )

    all_measurements = pd.concat(
        [
            measurements_2019,
            measurements_2020,
            measurements_2021,
            measurements_2022,
            measurements_2023,
        ]
    ).set_index("timestamp")

    all_measurements = all_measurements[
        [
            ("Schladen", 88.72),
            ("Ohrum", 75.54),
            ("sensoweb", "Schäferbr."),
            ("Eisenbütteler Wehr", "OW"),
            ("Petriwehr", "OW"),
            ("Wendenwehr", "OW"),
        ]
    ]

    all_measurements = all_measurements.rename(
        columns={
            ("Schladen", 88.72): "schladen",
            ("Ohrum", 75.54): "ohrum_level",
            ("sensoweb", "Schäferbr."): "schaeferbridge",
            ("Eisenbütteler Wehr", "OW"): "eisenbuetteler_wehr",
            ("Petriwehr", "OW"): "petriwehr",
            ("Wendenwehr", "OW"): "wendenwehr",
        }
    )

    all_measurements = all_measurements.replace("-", np.nan).bfill()

    return all_measurements

"""Testing Pipeline"""

weather_data_okertal = get_forecast("okertal")
weather_data_schladen = get_forecast("schladen")
weather_data_ohrum = get_forecast("ohrum")
weather_data_bridge = get_forecast("schaeferbruecke")
weather_data_eisenbuettel = get_forecast("eisenbuetteler_wehr")
weather_data_wendenwehr = get_forecast("wendenwehr")


# scaler1 = pickle.load("scaler1.pkl")
# scaler2 = pickle.load("scaler2.pkl")
# scaler3 = pickle.load("scaler3.pkl")
# scaler4 = pickle.load("scaler4.pkl")
# scaler5 = pickle.load("scaler5.pkl")
# scaler6 = pickle.load("scaler6.pkl")


with open("scaler1.pkl", "rb") as file:
    scaler1 = pickle.load(file)

with open("scaler2.pkl", "rb") as file:
    scaler2 = pickle.load(file)

with open("scaler3.pkl", "rb") as file:
    scaler3 = pickle.load(file)

with open("scaler4.pkl", "rb") as file:
    scaler4 = pickle.load(file)

with open("scaler5.pkl", "rb") as file:
    scaler5 = pickle.load(file)

with open("scaler6.pkl", "rb") as file:
    scaler6 = pickle.load(file)


def predict_okertal(weather_data_okertal):
    # weather_data_okertal.reset_index(inplace=True)
    # print(weather_data_okertal)
    # weather_data_okertal = weather_data_okertal.drop(columns=["timestamp"])

    pickle_file = "model_okertal.pkl"
    with open(pickle_file, 'rb') as file:
        loaded_model = pickle.load(file)

    scaled = scaler1.transform(weather_data_okertal)
    fill = loaded_model.predict(scaled)

    return fill


def predict_schladen(fill,weather_data_schladen):

    # weather_data_schladen.reset_index(inplace=True)
    # weather_data_schladen = weather_data_schladen.drop(columns=["timestamp"])
    fill_df = pd.DataFrame(fill, index=weather_data_schladen.index, columns=['fill_[mio.m³]'])
    combined_df = weather_data_schladen.join(fill_df, how="inner")

    pickle_file = "model_schladen.pkl"
    with open(pickle_file, 'rb') as file:
        loaded_model = pickle.load(file)

    scaled = scaler2.transform(combined_df)

    schladen = loaded_model.predict(scaled)
    return schladen

def predict_ohrum(schladen, weather_data_ohrum):

    # weather_data_ohrum.reset_index(inplace=True)
    # weather_data_ohrum = weather_data_ohrum.drop(columns=["timestamp"])

    fill_df = pd.DataFrame(schladen, index=weather_data_ohrum.index, columns=['schladen'])
    combined_df = weather_data_ohrum.join(fill_df, how="inner")

    pickle_file = "model_ohrum.pkl"
    with open(pickle_file, 'rb') as file:
        loaded_model = pickle.load(file)

    scaled = scaler3.transform(combined_df)
    ohrum = loaded_model.predict(scaled)
    return ohrum

def predict_bridge(ohrum, weather_data_bridge):

    # weather_data_bridge.reset_index(inplace=True)
    # weather_data_bridge = weather_data_bridge.drop(columns=["timestamp"])

    fill_df = pd.DataFrame(ohrum, index=weather_data_bridge.index, columns=['ohrum_level'])
    combined_df = weather_data_bridge.join(fill_df, how="inner")

    pickle_file = "model_bridge.pkl"
    with open(pickle_file, 'rb') as file:
        loaded_model = pickle.load(file)

    scaled = scaler4.transform(combined_df)
    bridge = loaded_model.predict(scaled)

    return bridge

def predict_eisenbuettel(bridge, weather_data_eisenbuettel):

    # weather_data_eisenbuettel.reset_index(inplace=True)
    # weather_data_eisenbuettel = weather_data_eisenbuettel.drop(columns=["timestamp"])
    fill_df = pd.DataFrame(bridge, index=weather_data_eisenbuettel.index, columns=['schaeferbridge'])
    combined_df = weather_data_eisenbuettel.join(fill_df, how="inner")

    pickle_file = "model_eisenbuettel.pkl"
    with open(pickle_file, 'rb') as file:
        loaded_model = pickle.load(file)

    scaled = scaler5.transform(combined_df)
    eisenbuettel = loaded_model.predict(scaled)

    return eisenbuettel

def predict_wendenwehr(eisenbuettel, weather_data_wendenwehr):

    # weather_data_wendenwehr.reset_index(inplace=True)
    # weather_data_wendenwehr = weather_data_wendenwehr.drop(columns=["timestamp"])
    fill_df = pd.DataFrame(eisenbuettel, index=weather_data_wendenwehr.index, columns=['eisenbuetteler_wehr'])
    combined_df = weather_data_wendenwehr.join(fill_df, how="inner")

    pickle_file = "model_wendenwehr.pkl"
    with open(pickle_file, 'rb') as file:
        loaded_model = pickle.load(file)

    scaled = scaler6.transform(combined_df)
    wendenwehr = loaded_model.predict(scaled)

    return wendenwehr

def forecast():
    # okertal
    okertal_weather = get_forecast("okertal")
    fill = predict_okertal(okertal_weather)

    # schladen
    schladen_weather = get_forecast("schladen")
    schladen = predict_schladen(fill, schladen_weather)

    # ohrum
    ohrum_weather = get_forecast("ohrum")
    ohrum = predict_ohrum(schladen, ohrum_weather)

    # schaeferbruecke
    schaeferbruecke_weather = get_forecast("schaeferbruecke")
    schaeferbruecke = predict_bridge(ohrum, schaeferbruecke_weather)

    # eisenbuetteler_wehr
    eisenbuetteler_wehr_weather = get_forecast("eisenbuetteler_wehr")
    eisenbuetteler_wehr = predict_eisenbuettel(schaeferbruecke, eisenbuetteler_wehr_weather)

    # wendenwehr
    wendenwehr_weather = get_forecast("wendenwehr")
    wendenwehr = predict_wendenwehr(eisenbuetteler_wehr, wendenwehr_weather)

    final_result = {
        "fill": fill.tolist(),
        "schladen": schladen.tolist(),
        "ohrum": ohrum.tolist(),
        "schaeferbruecke": schaeferbruecke.tolist(),
        "eisenbuetteler_wehr": eisenbuetteler_wehr.tolist(),
        "wendenwehr": wendenwehr.tolist()
    }

    with open("forecast.json", "w") as file:
        json.dump(final_result, file)
    return final_result

if __name__ == '__main__':
    forecast()

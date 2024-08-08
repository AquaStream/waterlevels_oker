import pandas as pd
import requests
import numpy as np
from datetime import datetime
from waterlevels_oker import utils
from waterlevels_oker.config import *


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

	params = {
		"date": datetime.now().date().isoformat(),
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
		"fallback_source_ids",
		"icon",
	]
	raw_data = raw_data.drop(columns=drop_cols)
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

	okertal_data = okertal_data.loc[:, "Stauinhalt Okertalsperre [Mio.m³]"].rename(
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

	ohrum_data = preprocess_brunswick_data().loc[:, "ohrum"]
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


# todo: forecasts funcs

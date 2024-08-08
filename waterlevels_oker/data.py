import pandas as pd
import requests
import numpy as np
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

	# Drop timezone from datetime index
	weather_raw.index = weather_raw.index.tz_localize(None)

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
		columns={"Waserstand relativ [cm]": "waterlevel relative [cm]"}
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
	ohrum_data.loc[ohrum_data["waterlevel relative [cm]"] == " ---"] = np.mean(
		[ohrum_data.loc["2017-12-31 23:00:00"], ohrum_data.loc["2018-01-01 01:00:00"]]
	)
	ohrum_data = ohrum_data.astype(dtype={"waterlevel relative [cm]": "float"})

	ohrum_data.to_csv(utils.get_processed_path("processed_ohrum_data.csv"))

	return ohrum_data


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

	all_measurements = all_measurements.rename(
		columns={("Eisenbütteler Wehr", "OW"): "eisenbuetteler_wehr"}
	)

	return all_measurements

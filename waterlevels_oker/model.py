from waterlevels_oker.data import get_forecast, preprocess_weather_data


def forecast():
	# okertal
	okertal_weather = get_forecast("okertal")

	okertal_weather = preprocess_weather_data(okertal_weather)

	# todo:
	# scale etc
	# okertal_model =
	# okertal_pred = okertal_model.predict(X)

	# schladen
	schladen_weather = get_forecast("schladen")
	schladen_weather = preprocess_weather_data(schladen_weather)

	full_schladen = schladen_weather.reset_index().join(okertal_pred)

	# todo:
	# scale etc
	# schladen_model =
	# schladen_pred =

	# ohrum
	ohrum_weather = get_forecast("ohrum")
	ohrum_weather = preprocess_weather_data(ohrum_weather)

	full_ohrum = ohrum_weather.reset_index().join(schladen_pred)

	# todo:
	# ohrum_model =
	# scale etc
	# ohrum_pred =

	# schaeferbruecke
	schaeferbruecke_weather = get_forecast("schaeferbruecke")
	schaeferbruecke_weather = preprocess_weather_data(schaeferbruecke_weather)

	full_schaeferbruecke = schaeferbruecke_weather.reset_index().join(ohrum_pred)

	# todo:
	# schaeferbruecke_model =
	# scale etc
	# schaeferbruecke_pred =

	# eisenbuetteler_wehr
	eisenbuetteler_wehr_weather = get_forecast("eisenbuetteler_wehr")
	eisenbuetteler_wehr_weather = preprocess_weather_data(eisenbuetteler_wehr_weather)

	full_eisenbuetteler_wehr = eisenbuetteler_wehr_weather.reset_index().join(
		schaeferbruecke_pred
	)

	# todo:
	# eisenbuetteler_model =
	# scale etc
	# eisenbuetteler_pred =

	# wendenwehr
	wendenwehr_weather = get_forecast("wendenwehr")
	wendenwehr_weather = preprocess_weather_data(wendenwehr_weather)

	full_wendenwehr = wendenwehr_weather.reset_index().join(eisenbuetteler_pred)

	# todo:
	# wendenwehr_model =
	# scale etc
	# wendenwehr_pred

	return wendenwehr_pred


def test_forecast_prediction(X):
	"""
	testing forecast prediction.

	Parameters
	----------
	X_test : _type_
		_description_
	y_true : _type_
		_description_
	"""

	# get training okertal with data also available in the wendenwehr training set,
	# split it, go through chain manually (?), at the end you can compare y_pred with y_true from the wendenwehr set

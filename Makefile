# download climate data
get_raw_weather_data:
	@python -c "from waterlevels_oker.data import get_raw_weather_data; get_raw_weather_data()"

preprocess_weather_data:
	@python -c "from waterlevels_oker.data import preprocess_weather_data; preprocess_weather_data()"

preprocess_raw_data:
	preprocess_weather_data

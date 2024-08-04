# download climate data
get_climate_data:
	@python -c "from waterlevels_oker.data import get_climate_data; get_climate_data()"

preprocess_raw_data:
	@python -c "from waterlevels_oker.data import preprocess_ohrum_data; preprocess_ohrum_data()"

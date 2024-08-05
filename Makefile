# download climate data
get_climate_data:
	@python -c "from waterlevels_oker.data import get_climate_data; get_climate_data()"

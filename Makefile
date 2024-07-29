# download climate data
get_climate_data:
	@python -c "from waterlevels_oker.data import get_climate_data; get_climate_data()"

# process raw climate data into single features
process_raw_data:
	@python -c "from waterlevels_oker.data import process_raw_data; process_raw_data()"

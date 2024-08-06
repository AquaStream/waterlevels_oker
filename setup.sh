#!/bin/bash
get_raw_weather_data() {
    python3 -c "from waterlevels_oker.data import get_raw_weather_data; get_raw_weather_data()"
}

setup() {
    curl -sSL https://install.python-poetry.org | python3 -
    source $(poetry env info --path)/bin/activate
    poetry install && poetry update
    get_raw_weather_data
}

setup

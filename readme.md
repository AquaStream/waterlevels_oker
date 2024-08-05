# About this project - WaterLevels Oker

Predicting the waterlevels of the German river Oker.

# Getting started

## Prerequisites
The following are prerequisites to run this codebase:
 - Python
 - Poetry


 ## Installation
1. Install the poetry environment
	```sh
	poetry install
	```
2. Download climate data
    ```sh
    make get_climate_data
    ```
3. Put oker data into `/data/raw`



## `data` vs `static` directories
The `data` directory is for storing raw data, processed data (produced by this code but not final) and output data.
The contents of these folders should not be tracked by git,
because they may contain sensitive information and may be large in size.

The `static` directory is for static (unchanging) data that is needed for the code to run and is not sensitive,
such as lookup tables. These need to be shared between developers using the code, and should be tracked by git.

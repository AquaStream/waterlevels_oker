import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import zipfile
import io
import os
import shutil
from waterlevels_oker import utils
from tqdm.auto import tqdm


def get_climate_data():
    # Remove old data
    folder = utils.get_raw_path("climate")
    if os.path.isdir(folder):
        for filename in os.listdir(folder):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print("Failed to delete %s. Reason: %s" % (file_path, e))

        print("Removed old climate data")

    # Download new climate data
    base_url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/"

    features = [
        "air_temperature",
        "cloud_type",
        "cloudiness",
        "dew_point",
        "extreme_wind",
        "moisture",
        "precipitation",
        "pressure",
        "soil_temperature",
        "solar",
        "sun",
        "visibility",
        "weather_phenomena",
        "wind",
        "wind_synop"
    ]

    def extract_zip(url):
        page = requests.get(url).content
        soup = BeautifulSoup(page, features="html.parser")
        zip_url = soup.find(string=re.compile("00662"))

        zip_file = requests.get(f"{url}/{zip_url}")

        with zipfile.ZipFile(io.BytesIO(zip_file.content)) as z:
            file = z.infolist()[-1]
            # Original filename format is "produkt_tu_stunde_20230125_20240727_00662.txt"
            # New filename format is "0230125_20240727_feature_csv"
            new_file_name =  f"{feature}_{'_'.join(file.filename.split('_')[3:5])}.csv"
            file.filename = new_file_name
            z.extract(file, utils.get_raw_path("climate"))
        return None


    for feature in tqdm(features):
        url_historical = f"{base_url}/{feature}/historical"
        url_recent = f"{base_url}/{feature}/recent"

        if feature == "solar":
            url = f"{base_url}/{feature}"
            extract_zip(url)
        else:
            for url in [url_historical, url_recent]:
                extract_zip(url)

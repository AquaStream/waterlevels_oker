import pandas as pd
from bs4 import BeautifulSoup
import re
import requests
import zipfile
import io
import os
import re
import shutil
from waterlevels_oker import utils
from waterlevels_oker.config import *
from tqdm.auto import tqdm


def get_climate_data():
    """
    Removes old raw climate data, then downloads new one from opendata.dwd.de.
    """

    # Remove old data
    folder = utils.get_raw_path("climate")
    if not os.path.exists(folder):
        os.mkdir(folder)

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

    def extract_zip(url):
        page = requests.get(url).content
        soup = BeautifulSoup(page, features="html.parser")
        zip_url = soup.find(string=re.compile("00662"))

        zip_file = requests.get(f"{url}/{zip_url}")

        with zipfile.ZipFile(io.BytesIO(zip_file.content)) as z:
            file = z.infolist()[-1]
            # Original filename format is "produkt_tu_stunde_20230125_20240727_00662.txt"
            # New filename format is "0230125_20240727_feature_csv"
            new_file_name = f"{feature}_{'_'.join(file.filename.split('_')[3:5])}.csv"
            file.filename = new_file_name
            z.extract(file, utils.get_raw_path("climate"))

    for feature in tqdm(FEATURES):
        url_historical = f"{base_url}/{feature}/historical"
        url_recent = f"{base_url}/{feature}/recent"

        if feature == "solar":
            url = f"{base_url}/{feature}"
            extract_zip(url)
        else:
            for url in [url_historical, url_recent]:
                extract_zip(url)


def process_raw_data():
    """
    Process raw historical and recent csv into a single feature csv
    """
    for feature in tqdm(FEATURES):
        files_list = [
            file
            for file in os.listdir(utils.get_raw_path("climate"))
            if re.match(fr"^{feature}_\d", file)
        ]
        data_list = []
        for file in files_list:
            try:
                data = pd.read_csv(utils.get_raw_path(f"climate/{file}"), sep=";", low_memory=False)
                data.columns = [col.strip() for col in data.columns]
            except UnicodeDecodeError:
                data = pd.read_csv(utils.get_raw_path(f"climate/{file}"), sep=";", low_memory=False, encoding="latin_1")
                data.columns = [col.strip() for col in data.columns]

            # drop first and last columns, as they only specify the station id and end of row
            data = data.iloc[:, 1:-1]
            data_list.append(data)
        concat_data = pd.concat(data_list)
        no_duplicates = concat_data.drop_duplicates()
        processed_path = utils.get_processed_path("climate")
        if not os.path.exists(processed_path):
            os.mkdir(processed_path)
        no_duplicates.to_csv(f"{processed_path}/{feature}.csv", index=False)

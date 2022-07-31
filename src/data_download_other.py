"""Downloading data from other sources

Sectoral Marine Plan for Offshore Wind Energy Draft Plan Options
Data by Marine Scotland (https://marine.gov.scot/):
https://marine.gov.scot/data/sectoral-marine-plan-offshore-wind-energy-draft-plan-options-gis-files
Format: Shapefile
Version: 01/2020

Historic Environment Scotland - Scheduled Monuments:
https://portal.historicenvironment.scot/downloads
Format: Shapefile

Community Council Areas:
https://data.spatialhub.scot/dataset/community_council_boundaries-is
Format: Shapefile

OS British National Grids from GitHub:
https://github.com/OrdnanceSurvey/OS-British-National-Grids

Based on catalogue searches: https://www.spatialdata.gov.scot
"""

# import libraries
import os
import xml.etree.ElementTree as ET
import requests

# ##########################################################################
# base data download directory
BASE_DIR_DEF = os.path.join("data", "raw")


# ##########################################################################
# define function to download data
def download_data(
    server, subdir, params=None, basedir=BASE_DIR_DEF, chunk_size=1048676
):
    """
    Download data using specified URL and optional parameters into
    the specified directory
    Parameters:
    -----------
    `server`: data download URL
    `subdir`: subdirectory where the downloaded files will be stored
    `params`: optional request parameters; default is None
    `basedir`: base data download directory; default is "data/raw"
    `chunk_size`: number of bytes of data per downloaded chunk; default is
                  1048676
    """
    # get request
    r_dd = requests.get(server, params=params, stream=True)
    # create directory to store files
    download_dir = os.path.join(basedir, subdir)
    os.makedirs(download_dir, exist_ok=True)
    # download data to directory
    if r_dd.status_code == 200:
        if r_dd.headers["content-type"] == "application/zip":
            file_name = "data.zip"
        elif r_dd.headers["content-type"][0:8] == "text/xml":
            file_name = "data.gml"
        else:
            file_name = "data"
        with open(os.path.join(download_dir, file_name), "wb") as file_dd:
            for chunk in r_dd.iter_content(chunk_size=chunk_size):
                file_dd.write(chunk)
        print("Data successfully downloaded to", download_dir)
    else:
        print(
            "Data not downloaded to", download_dir,
            "\nStatus code:", r_dd.status_code
        )


# function to download NatureScot data
def download_data_ns(dataset, subdir):
    """Download NatureScot Natural Spaces data
    Parameters:
    -----------
    `dataset`: name of the dataset to be downloaded
    `subdir`: subdirectory where the downloaded files will be stored
    """
    base_url_def = (
        "https://gateway.snh.gov.uk/natural-spaces/inspire_download.atom.xml"
    )
    payload_dd = {"code": dataset}
    r_dd = requests.get(base_url_def, params=payload_dd)
    if r_dd.status_code == 200:
        root = ET.fromstring(r_dd.content)
        data_url = root[11][3].text
        download_data(server=data_url, subdir=subdir)
    else:
        print("Error! Status code:", r_dd.status_code)

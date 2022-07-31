"""Download Ordnance Survey Open Data using the OS Downloads API

See the API documentation here:
https://osdatahub.os.uk/docs/downloads/overview.

The download URL is generally of this format:
https://api.os.uk/downloads/v1/products/
${id}/downloads?area=${area}&format=${format}&redirect

See https://osdatahub.os.uk/downloads/open for the list of available open
datasets, their formats, and area coverage.
"""

# import libraries
import os
import requests

# ##########################################################################
# base directory to download data
BASE_DIR_DEF = os.path.join("data", "raw")

# server base URL
SERV_DEF = "https://api.os.uk/downloads/v1/products"


# ##########################################################################
def data_keys(server=SERV_DEF):
    """Return the list of data keys for a given server URL
    Parameters:
    -----------
    `server`: server URL; default is "https://api.os.uk/downloads/v1/products"
    """
    r_dk = requests.get(server)
    if r_dk.status_code == 200:
        return list(r_dk.json()[0].keys())
    else:
        print("Error! Status code:", r_dk.status_code)


def data_products():
    """Returns a list of the OS OpenData products available to download
    """
    r_dp = requests.get(SERV_DEF)
    id_list = []
    version_list = []
    if r_dp.status_code == 200:
        for i in range(len(r_dp.json())):
            id_list.append(r_dp.json()[i]["id"])
            version_list.append(r_dp.json()[i]["version"])
        for row in zip(id_list, version_list):
            print(" ".join(row))
    else:
        print("Error! Status code:", r_dp.status_code)


# function to list a particular dataset's specifications
def data_specs(dataset):
    """Print dataset specifications using the Ordnance Survey Downloads API
    Parameters:
    -----------
    `dataset`: name of dataset
    """
    r_ds = requests.get(SERV_DEF + "/" + dataset + "/downloads")
    if r_ds.status_code == 200:
        formats = []
        areas = []
        for i in range(len(r_ds.json())):
            formats.append(r_ds.json()[i]["format"])
            areas.append(r_ds.json()[i]["area"])
        print(
            "Formats: " + str(set(formats)) + "\nAreas: " + str(set(areas))
        )
    else:
        print("Error! Status code:", r_ds.status_code)


# function to download data for a particular area and format
def data_download(
    dataset, subdir, area, dataformat,
    basedir=BASE_DIR_DEF, chunk_size=1048676
):
    """Download Ordnance Survey Open Data using the Downloads API
    Parameters:
    -----------
    `dataset`: name of dataset
    `subdir`: sub directory within the base directory to store files
    `area`: area of interest
    `dataformat`: format of data to be downloaded
    `basedir`: base data download directory; default is "data/raw"
    `chunk_size`: number of bytes of data per downloaded chunk; default is
                  1048676
    """
    payload = {"area": area, "format": dataformat, "redirect": ""}
    r_dd = requests.get(
        SERV_DEF + "/" + dataset + "/downloads", params=payload, stream=True
    )
    if r_dd.status_code == 200:
        download_dir = os.path.join(basedir, subdir)
        os.makedirs(download_dir, exist_ok=True)
        with open(os.path.join(download_dir, "data.zip"), "wb") as file_dd:
            for chunk in r_dd.iter_content(chunk_size=chunk_size):
                file_dd.write(chunk)
        print("Data successfully downloaded to", download_dir)
    else:
        print(
            "Data not downloaded to", download_dir,
            "\nStatus code:", r_dd.status_code
        )

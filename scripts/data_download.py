"""Downloading data

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
import glob
import os
import xml.etree.ElementTree as ET
from io import BytesIO
from zipfile import ZipFile
import requests

# ##########################################################################
# base data download directory
basedir = "data/raw/"


# define function to download data
def downloadData(url, subdir, params=None):
    """
    Download data using specified URL and optional parameters into
    the specified directory
    Parameters:
    -----------
    `url`: download URL \\
    `subdir`: subdirectory where the downloaded files will be stored \\
    `params`: optional request parameters
    """
    # get request
    r = requests.get(url, params=params)
    # create directory to store files
    downloadDir = basedir + subdir
    os.makedirs(downloadDir, exist_ok=True)
    # download data to directory
    if r.status_code == 200:
        z = ZipFile(BytesIO(r.content))
        z.extractall(downloadDir)
        print("Data successfully downloaded to", downloadDir)
    else:
        print(
            "Data not downloaded to", downloadDir,
            "\nStatus code:", r.status_code
        )


# ######################################################################
# Sectoral Marine Plan options
url = "https://msmap1.atkinsgeospatial.com/geoserver/nmpwfs/ows"

# define request parameters
payload = {
    "token": "d46ffd2a-e192-4e51-8a6a-b3292c20f1ee",
    "service": "wfs",
    "request": "getFeature",
    "typeName": "nmpwfs:energy_resources_smp_wind_plan_options",
    "outputFormat": "shape-zip",
    "srsName": "EPSG:4326"
}

subdir = "marine/smp/"

downloadData(url, subdir, params=payload)

# ######################################################################
# Historic Environment Scotland - Scheduled monuments
url = "https://inspire.hes.scot/AtomService/DATA/sam_scotland.zip"

subdir = "cultural/sam/"

downloadData(url, subdir)

# ######################################################################
# NatureScot
baseurl = (
    "https://gateway.snh.gov.uk/natural-spaces/inspire_download.atom.xml?code="
)

# GeMS - Scottish Priority Marine Features (PMF)
r = requests.get(baseurl + "GEMS-PMF")
if r.status_code == 200:
    root = ET.fromstring(r.content)
    url = root[11][3].text
    subdir = "natural/gems_pmf"
    downloadData(url, subdir)

# Marine Consultation Areas (MCA)
r = requests.get(baseurl + "MCA")
if r.status_code == 200:
    root = ET.fromstring(r.content)
    url = root[11][3].text
    subdir = "natural/mca"
    downloadData(url, subdir)

# ######################################################################
# National Scenic Areas
url = (
    "https://maps.gov.scot/ATOM/shapefiles/SG_NationalScenicAreas_1998.zip"
)

subdir = "natural/nsa/"

downloadData(url, subdir)

# ######################################################################
# Community council areas
url = "https://geo.spatialhub.scot/geoserver/sh_commcnc/wfs"

payload = {
    "authkey": "b85aa063-d598-4582-8e45-e7e6048718fc",
    "request": "GetFeature",
    "service": "WFS",
    "version": "1.1.0",
    "typeName": "pub_commcnc",
    "outputFormat": "SHAPE-ZIP"
}

downloadDir = "administrative/ccb/"

downloadData(url, subdir, params=payload)

# ######################################################################
# Ordnance Survey BNG
url = (
    "https://github.com/OrdnanceSurvey/OS-British-National-Grids/archive/" +
    "main.zip"
)

subdir = "administrative/os_bng/"

downloadData(url, subdir)

# extract BNG data using 7zip
os.system(
    "7z e " + glob.glob(basedir + subdir + "/*/*.7z")[0] +
    " -o" + basedir + subdir
)

# ######################################################################
# National Records of Scotland - Output Areas 2011
# Population weighted centroids

url = "https://www.nrscotland.gov.uk/files/geography/output-area-2011-pwc.zip"

subdir = "administrative/census_centroids/"

downloadData(url, subdir)

# Population boundaries
url = "https://www.nrscotland.gov.uk/files/geography/output-area-2011-eor.zip"

subdir = "administrative/census_areas/"

downloadData(url, subdir)

# Census 2011
url = (
    "https://nrscensusprodumb.blob.core.windows.net/downloads/" +
    "Output Area blk.zip"
)

subdir = "administrative/census_data/"

downloadData(url, subdir)

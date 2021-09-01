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
from zipfile import ZipFile
import requests

# ##########################################################################
# base directory to download data
basedir = "data/raw/"

# server base URL
serv = "https://api.os.uk/downloads/v1/products"

# get list of product IDs
r = requests.get(serv)

idList = []
versionList = []
if r.status_code == 200:
    # get the list of keys available for each dataset
    list(r.json()[0].keys())
    # ['id', 'name', 'description', 'version', 'url']
    for i in range(len(r.json())):
        idList.append(r.json()[i]["id"])
        versionList.append(r.json()[i]["version"])

list(zip(idList, versionList))
# [('250kScaleColourRaster', '2021-06'), ('BoundaryLine', '2021-05'),
# ('CodePointOpen', '2021-08'), ('GBOverviewMaps', '2014-11'),
# ('LIDS', '2021-08'), ('MiniScale', '2021-01'),
# ('OpenGreenspace', '2021-04'), ('OpenMapLocal', '2021-04'),
# ('OpenNames', '2021-07'), ('OpenRivers', '2021-04'),
# ('OpenRoads', '2021-04'), ('OpenTOID', '2021-07'),
# ('OpenUPRN', '2021-08'), ('OpenUSRN', '2021-08'),
# ('OpenZoomstack', '2021-06'), ('Strategi', '2016-01'),
# ('Terrain50', '2021-07'), ('VectorMapDistrict', '2021-05')]

# list of keys available
r = requests.get(serv + "/BoundaryLine/downloads")
if r.status_code == 200:
    list(r.json()[0].keys())
    # ['md5', 'size', 'url', 'format', 'area', 'fileName']


# function to list a particular dataset's specifications
def dataspecs(dataset):
    r = requests.get(serv + "/" + dataset + "/downloads")
    if r.status_code == 200:
        formats = []
        areas = []
        for i in range(len(r.json())):
            formats.append(r.json()[i]["format"])
            areas.append(r.json()[i]["area"])
        print(
            "Formats: " + str(set(formats)) + "\nAreas: " + str(set(areas))
        )


# function to download data for a particular area and format
def dataDownload(dataset, subdir, area, dataformat, chunk_size=1048676):
    """Download Ordnance Survey Open Data using the Downloads API
    Parameters:
    -----------
    `dataset`: name of dataset \\
    `subdir`: sub directory within the base directory to store files \\
    `area`: area of interest \\
    `dataformat`: format of data to be downloaded \\
    `chunk_size`: number of bytes of data per downloaded chunk
    """
    payload = {"area": area, "format": dataformat, "redirect": ""}
    r = requests.get(
        serv + "/" + dataset + "/downloads", params=payload, stream=True
    )
    if r.status_code == 200:
        downloadDir = basedir + subdir
        os.makedirs(downloadDir, exist_ok=True)
        with open(downloadDir + dataset + ".zip", "wb") as fd:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
        z = ZipFile(downloadDir + dataset + ".zip")
        z.extractall(downloadDir)
        print("Data successfully downloaded to", downloadDir)
    else:
        print(
            "Data not downloaded to", downloadDir,
            "Status code:", r.status_code
        )


# Downloading BoundaryLine
dataspecs(dataset="BoundaryLine")
# Formats: {'GML', 'Vector Tiles', 'MapInfo® TAB', 'ESRI® Shapefile',
# 'GeoPackage'}
# Areas: {'GB'}
dataDownload(
    dataset="BoundaryLine",
    subdir="administrative/os_bdline/",
    area="GB",
    dataformat="GeoPackage"
)

dataspecs(dataset="Terrain50")
# Formats: {'GeoPackage', 'ESRI® Shapefile', 'GML',
# 'ASCII Grid and GML (Grid)'}
# Areas: {'GB'}
dataDownload(
    dataset="Terrain50",
    subdir="elevation/os_terrain50/",
    area="GB",
    dataformat="GeoPackage"
)

dataspecs(dataset="OpenNames")
# Formats: {'CSV', 'GML', 'GeoPackage'}
# Areas: {'GB'}
dataDownload(
    dataset="OpenNames",
    subdir="administrative/os_opennames/",
    area="GB",
    dataformat="CSV"
)

# dataspecs(dataset="250kScaleColourRaster")
# # Formats: {'TIFF-LZW'}
# # Areas: {'GB'}
# dataDownload(
#     dataset="250kScaleColourRaster",
#     subdir="rasters/os_250kraster/",
#     area="GB",
#     dataformat="TIFF-LZW"
# )

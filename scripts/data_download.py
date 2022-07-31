"""Download all required datasets
"""

# import libraries
import os
from zipfile import ZipFile
import py7zr
from src import data_download_os as ddos
from src import data_download_other as dd

# OS data from the Downloads API # ---------------------------------------

# Boundary-Line -----------------------------
ddos.data_download(
    dataset="BoundaryLine",
    subdir=os.path.join("vector", "os_bdline"),
    area="GB",
    dataformat="GeoPackage"
)

# Terrain 50 -------------------------------
ddos.data_download(
    dataset="Terrain50",
    subdir=os.path.join("vector", "os_terrain50"),
    area="GB",
    dataformat="GeoPackage"
)

# OpenNames --------------------------------
ddos.data_download(
    dataset="OpenNames",
    subdir=os.path.join("vector", "os_opennames"),
    area="GB",
    dataformat="CSV"
)

# 250kScaleColourRaster --------------------
ddos.data_download(
    dataset="250kScaleColourRaster",
    subdir=os.path.join("raster", "os_250kraster"),
    area="GB",
    dataformat="TIFF-LZW"
)

# Data from other sources # ----------------------------------------------

# Sectoral Marine Plan ---------------------
URL = "https://msmap1.atkinsgeospatial.com/geoserver/nmpwfs/ows"
payload = {
    "token": "d46ffd2a-e192-4e51-8a6a-b3292c20f1ee",
    "service": "wfs",
    "request": "getFeature",
    "typeName": "nmpwfs:energy_resources_smp_wind_plan_options",
    "outputFormat": "shape-zip",
    "srsName": "EPSG:4326"
}
dd.download_data(
    server=URL, subdir=os.path.join("vector", "ms_smp"), params=payload
)

# HES Scheduled monuments ------------------
URL = "https://inspire.hes.scot/AtomService/DATA/sam_scotland.zip"
dd.download_data(server=URL, subdir=os.path.join("vector", "hes_sam"))

# National Scenic Areas --------------------
URL = "https://maps.gov.scot/ATOM/shapefiles/SG_NationalScenicAreas_1998.zip"
dd.download_data(server=URL, subdir=os.path.join("vector", "sg_nsa"))

# Community council areas ------------------
URL = "https://geo.spatialhub.scot/geoserver/sh_commcnc/wfs"
payload = {
    "authkey": "b85aa063-d598-4582-8e45-e7e6048718fc",
    "request": "GetFeature",
    "service": "WFS",
    "typeName": "pub_commcnc",
    "format_options": "filename:Community_Council_Boundaries_-_Scotland",
    "outputFormat": "shape-zip"
}
dd.download_data(
    server=URL, subdir=os.path.join("vector", "is_ccb"), params=payload
)

# Ordnance Survey BNG ----------------------
URL = (
    "https://github.com/OrdnanceSurvey/OS-British-National-Grids/archive/" +
    "main.zip"
)
dd.download_data(server=URL, subdir=os.path.join("vector", "os_bng"))

# extract the GPKG from the 7z archive
ZIP_FILE = os.path.join(dd.BASE_DIR_DEF, "vector", "os_bng", "data.zip")
archive = ZipFile(ZIP_FILE, "r")
files = [name for name in archive.namelist() if name.endswith(".7z")]
if len(files) == 1:
    with archive.open(files[0]) as sz:
        szarchive = py7zr.SevenZipFile(sz, mode="r")
        szarchive.extractall(
            path=os.path.join(dd.BASE_DIR_DEF, "vector", "os_bng")
        )
        szarchive.close()

# NRS - Output Areas 2011 ------------------
# Population weighted centroids
URL = (
    "https://maps.gov.scot/server/services/NRS/Census2011/MapServer/WFSServer"
)
payload = {
    "request": "GetFeature",
    "service": "WFS",
    "version": "1.1.0",
    "typeName": "CEN2011:OutputAreaCent2011",
    "outputFormat": "GML3"
}
dd.download_data(
    server=URL,
    subdir=os.path.join("vector", "census_centroids"),
    params=payload
)

# Population boundaries
URL = (
    "https://maps.gov.scot/server/services/NRS/Census2011/MapServer/WFSServer"
)
payload = {
    "request": "GetFeature",
    "service": "WFS",
    "version": "1.1.0",
    "typeName": "CEN2011:OutputArea2011",
    "outputFormat": "GML3"
}
dd.download_data(
    server=URL, subdir=os.path.join("vector", "census_areas"), params=payload
)

# Census 2011
URL = (
    "https://nrscensusprodumb.blob.core.windows.net/downloads/" +
    "Output Area blk.zip"
)
dd.download_data(server=URL, subdir=os.path.join("vector", "census_data"))

# NatureScot -------------------------------
# GeMS - Scottish Priority Marine Features (PMF)
dd.download_data_ns(
    dataset="GEMS-PMF", subdir=os.path.join("vector", "ns_gems_pmf")
)

# Marine Consultation Areas (MCA)
dd.download_data_ns(dataset="MCA", subdir=os.path.join("vector", "ns_mca"))

"""Defining the study area
"""

# import libraries
import os
from zipfile import ZipFile
import fiona
import pandas as pd
import geopandas as gpd

# define/create data directories
BASE_PATH = os.path.join("data", "raw", "vector")
OUT_PATH = os.path.join("data", "vector")
os.makedirs(OUT_PATH, exist_ok=True)

# Sectoral Marine Plan options --------------------------------------
ZIP_FILE = os.path.join(BASE_PATH, "ms_smp", "data.zip")
archive = ZipFile(ZIP_FILE, "r")
files = [name for name in archive.namelist() if name.endswith(".shp")]

smp = gpd.read_file("zip://" + ZIP_FILE + "!" + files[0])

if smp.crs != 27700:
    smp = smp.to_crs("epsg:27700")

# keep only N4
N4 = smp.loc[smp["name"] == "N4"]

# study area buffer
study_area = gpd.GeoDataFrame(geometry=N4.buffer(15000), crs="EPSG:27700")
study_area["Name"] = (
    "Study area boundary around Sectoral Marine Plan option N4"
)

# save to GPKG
GPKG_FILE = os.path.join(OUT_PATH, "boundaries.gpkg")
smp.to_file(
    GPKG_FILE, layer="sectoral_marine_plan", driver="GPKG", index=False
)
N4.to_file(
    GPKG_FILE, layer="sectoral_marine_plan_N4", driver="GPKG", index=False
)
study_area.to_file(
    GPKG_FILE, layer="study_area", driver="GPKG", index=False
)

# OS Boundary-Line ---------------------------------------------------
ZIP_FILE = os.path.join(BASE_PATH, "os_bdline", "data.zip")
archive = ZipFile(ZIP_FILE, "r")
files = [name for name in archive.namelist() if name.endswith(".gpkg")]

bd_line = gpd.read_file(
    "zip://" + ZIP_FILE + "!" + files[0], layer="scotland_and_wales_const"
)

bd_line = bd_line.loc[bd_line["Area_Code"] == "SPC"]

# dissolve boundaries
scotland = bd_line.dissolve(by="Area_Code")
scotland["Name"] = "Scotland"
scotland = scotland[["Name", "geometry"]]

# Western Isles
w_isles = bd_line.loc[bd_line["Name"] == "Na h-Eileanan an Iar P Const"]

# save as GPKG layers
bd_line.to_file(
    GPKG_FILE, layer="os_bdline_scotland_const", driver="GPKG", index=False
)
scotland.to_file(
    GPKG_FILE, layer="os_bdline_scotland", driver="GPKG", index=False
)
w_isles.to_file(
    GPKG_FILE, layer="os_bdline_westernisles_const", driver="GPKG", index=False
)

# Community council boundaries --------------------------------------
ZIP_FILE = os.path.join(BASE_PATH, "is_ccb", "data.zip")
archive = ZipFile(ZIP_FILE, "r")
files = [name for name in archive.namelist() if name.endswith(".shp")]

ccb = gpd.read_file(
    "zip://" + ZIP_FILE + "!" + files[0],
    bbox=(8e4, 8.95e5, 1.6e5, 9.8e5)
)

ccb.to_file(GPKG_FILE, layer="community_council", driver="GPKG", index=False)

# OS British National Grids -----------------------------------------
FILE_NAME = os.path.join(BASE_PATH, "os_bng", "os_bng_grids.gpkg")
layers = fiona.listlayers(FILE_NAME)

bng = {}
for layer in layers:
    bng[layer] = gpd.read_file(FILE_NAME, layer=layer, bbox=scotland)

for layer in layers:
    bng[layer].to_file(
        os.path.join(OUT_PATH, "context.gpkg"),
        layer=layer, driver="GPKG", index=False
    )

# OS Open Names -----------------------------------------------------
ZIP_FILE = os.path.join(BASE_PATH, "os_opennames", "data.zip")
archive = ZipFile(ZIP_FILE, "r")
files = [
    name for name in archive.namelist() if "NA8" in name or "NB" in name and
    name.endswith(".csv")
]
files = files[:-1]

headers = gpd.read_file(
    "zip://" + ZIP_FILE + "!" +
    os.path.join("Docs", "OS_Open_Names_Header.csv")
)

opennames = pd.DataFrame()
for layer in files:
    names = gpd.read_file("zip://" + ZIP_FILE + "!" + layer)
    opennames = pd.concat([opennames, names])
opennames.columns = list(headers)

# well known text with point data
opennames["wkt"] = (
    "POINT (" + opennames["GEOMETRY_X"].astype(str) + " " +
    opennames["GEOMETRY_Y"].astype(str) + ")"
)

opennames = gpd.GeoDataFrame(
    opennames,
    geometry=gpd.GeoSeries.from_wkt(opennames["wkt"]),
    crs="EPSG:27700"
)

opennames = opennames.drop(columns=["wkt"])

opennames.to_file(
    os.path.join(OUT_PATH, "context.gpkg"),
    layer="os_opennames", driver="GPKG", index=False
)

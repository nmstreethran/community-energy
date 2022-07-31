"""Producing a DTM using TIN interpolation

This is a standalone script which can be run outside of the QGIS Python
console in the QGIS Anaconda virtual environment.

Prerequisite: Download EMODnet Bathymetry data covering the study area and
store it in this file path: "data/raw/rasters/bathymetry.asc"
"""

# set paths to QGIS libraries
# may be necessary if using Windows
# exec(open("scripts/set_sys_paths.py").read())

# import libraries
from qgis.core import (
    QgsApplication, QgsProcessingFeedback, QgsCoordinateReferenceSystem
)

# create a reference to the QgsApplication
# setting the second argument to False disables the GUI
qgs = QgsApplication([], False)

# load providers
qgs.initQgis()

# import processing libraries
from qgis import processing
from processing.core.Processing import Processing
Processing.initialize()

# ######################################################################
import os
import geopandas as gpd

# path to GeoPackage with input layers and data folders
GPKG_PATH = "data/input.gpkg"
TEMP_DIR = "data/temp/dtm/"
RASTER_DIR = "data/rasters/"

# create directory to store temporary files
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(RASTER_DIR, exist_ok=True)

feedback = QgsProcessingFeedback()

# convert bathymetry raster to points
params = {
    "INPUT_RASTER": "data/raw/rasters/bathymetry.asc",
    "RASTER_BAND": 1,
    "FIELD_NAME": "VALUE",
    "OUTPUT": TEMP_DIR + "bathymetry_pts_temp.shp"
}
processing.run("native:pixelstopoints", params, feedback=feedback)

# assign projection
params = {
    "INPUT": TEMP_DIR + "bathymetry_pts_temp.shp",
    "CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
    "OUTPUT": TEMP_DIR + "bathymetry_pts_wgs84.shp"
}
processing.run("native:assignprojection", params, feedback=feedback)

# reproject points from WGS84 to OSGB 1936
params = {
    "INPUT": TEMP_DIR + "bathymetry_pts_wgs84.shp",
    "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:27700"),
    "OUTPUT": TEMP_DIR + "bathymetry_pts_osgb.shp"
}
processing.run("native:reprojectlayer", params, feedback=feedback)

# clip points to study area
# outLayer = (
#     "ogr:dbname=\'" + GPKG_PATH + "\' table=\"emodnet_bathymetry\" (geom)"
# )
# params = {
#     "INPUT": TEMP_DIR + "bathymetry_pts_osgb.shp",
#     "MASK": GPKG_PATH + "|layername=study_area_water",
#     "OUTPUT": outLayer
# }
# processing.run("gdal:clipvectorbypolygon", params, feedback=feedback)

data = gpd.read_file(
    TEMP_DIR + "bathymetry_pts_osgb.shp",
    mask=gpd.read_file(GPKG_PATH, layer="study_area_water")
)
data.to_file(GPKG_PATH, layer="emodnet_bathymetry", driver="GPKG")

# define data sources
EXTENT_LAYER = GPKG_PATH + "|layername=study_area"
SPOTHEIGHT_LAYER = GPKG_PATH + "|layername=os_terrain50_spotheight"
CONTOUR_LAYER = GPKG_PATH + "|layername=os_terrain50_contourline"
BOUNDARY_LAYER = GPKG_PATH + "|layername=os_terrain50_landwaterboundary"
BATHYMETRY_LAYER = GPKG_PATH + "|layername=emodnet_bathymetry"

# define TIN interpolation data
INTERPOLATION_DATA = (
    BATHYMETRY_LAYER + "::~::0::~::0::~::0::|::" +
    SPOTHEIGHT_LAYER + "::~::0::~::2::~::0::|::" +
    CONTOUR_LAYER + "::~::0::~::2::~::1::|::" +
    BOUNDARY_LAYER + "::~::0::~::2::~::2"
)

# TIN interpolation
params = {
    "INTERPOLATION_DATA": INTERPOLATION_DATA,
    "EXTENT": EXTENT_LAYER,
    "PIXEL_SIZE": 10,
    "OUTPUT": TEMP_DIR + "terrain_temp.tif",
    "TRIANGULATION": TEMP_DIR + "terrain_tin.shp"
}
processing.run("qgis:tininterpolation", params, feedback=feedback)

# clip to study area
params = {
    "INPUT": TEMP_DIR + "terrain_temp.tif",
    "MASK": EXTENT_LAYER,
    "OUTPUT": RASTER_DIR + "terrain.tif"
}
processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

# clip DTM to N4
params = {
    "INPUT": RASTER_DIR + "terrain.tif",
    "MASK": GPKG_PATH + "|layername=sectoral_marine_plan_N4",
    "OUTPUT": RASTER_DIR + "terrain_N4.tif"
}
processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

# ######################################################################
# call exitQgis() to remove the provider and layer registries from memory
qgs.exitQgis()

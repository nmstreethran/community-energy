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
gpkgPath = "data/input.gpkg"
tempDir = "data/temp/dtm/"
rasterDir = "data/rasters/"

# create directory to store temporary files
os.makedirs(tempDir, exist_ok=True)
os.makedirs(rasterDir, exist_ok=True)

feedback = QgsProcessingFeedback()

# convert bathymetry raster to points
params = {
    "INPUT_RASTER": "data/raw/rasters/bathymetry.asc",
    "RASTER_BAND": 1,
    "FIELD_NAME": "VALUE",
    "OUTPUT": tempDir + "bathymetry_pts_temp.shp"
}
processing.run("native:pixelstopoints", params, feedback=feedback)

# assign projection
params = {
    "INPUT": tempDir + "bathymetry_pts_temp.shp",
    "CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
    "OUTPUT": tempDir + "bathymetry_pts_wgs84.shp"
}
processing.run("native:assignprojection", params, feedback=feedback)

# reproject points from WGS84 to OSGB 1936
params = {
    "INPUT": tempDir + "bathymetry_pts_wgs84.shp",
    "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:27700"),
    "OUTPUT": tempDir + "bathymetry_pts_osgb.shp"
}
processing.run("native:reprojectlayer", params, feedback=feedback)

# clip points to study area
# outLayer = (
#     "ogr:dbname=\'" + gpkgPath + "\' table=\"emodnet_bathymetry\" (geom)"
# )
# params = {
#     "INPUT": tempDir + "bathymetry_pts_osgb.shp",
#     "MASK": gpkgPath + "|layername=study_area_water",
#     "OUTPUT": outLayer
# }
# processing.run("gdal:clipvectorbypolygon", params, feedback=feedback)

data = gpd.read_file(
    tempDir + "bathymetry_pts_osgb.shp",
    mask=gpd.read_file(gpkgPath, layer="study_area_water")
)
data.to_file(gpkgPath, layer="emodnet_bathymetry", driver="GPKG")

# define data sources
extentLayer = gpkgPath + "|layername=study_area"
spotheightLayer = gpkgPath + "|layername=os_terrain50_spotheight"
contourLayer = gpkgPath + "|layername=os_terrain50_contourline"
boundaryLayer = gpkgPath + "|layername=os_terrain50_landwaterboundary"
bathymetryLayer = gpkgPath + "|layername=emodnet_bathymetry"

# define TIN interpolation data
interpolationData = (
    bathymetryLayer + "::~::0::~::0::~::0::|::" +
    spotheightLayer + "::~::0::~::2::~::0::|::" +
    contourLayer + "::~::0::~::2::~::1::|::" +
    boundaryLayer + "::~::0::~::2::~::2"
)

# TIN interpolation
params = {
    "INTERPOLATION_DATA": interpolationData,
    "EXTENT": extentLayer,
    "PIXEL_SIZE": 10,
    "OUTPUT": tempDir + "terrain_temp.tif",
    "TRIANGULATION": tempDir + "terrain_tin.shp"
}
processing.run("qgis:tininterpolation", params, feedback=feedback)

# clip to study area
params = {
    "INPUT": tempDir + "terrain_temp.tif",
    "MASK": extentLayer,
    "OUTPUT": rasterDir + "terrain.tif"
}
processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

# clip DTM to N4
params = {
    "INPUT": rasterDir + "terrain.tif",
    "MASK": gpkgPath + "|layername=sectoral_marine_plan_N4",
    "OUTPUT": rasterDir + "terrain_N4.tif"
}
processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

# ######################################################################
# call exitQgis() to remove the provider and layer registries from memory
qgs.exitQgis()

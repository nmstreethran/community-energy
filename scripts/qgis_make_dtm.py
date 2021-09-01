"""Producing a DTM using TIN interpolation

This is a standalone script which can be run outside of the QGIS Python
console in the QGIS Anaconda virtual environment.

Prerequisite: Download EMODnet Bathymetry data covering the study area and
store it in this file path: "data/raw/rasters/bathymetry.asc"
"""

# set paths to QGIS libraries
# required for Windows
exec(open("set_sys_paths.py").read())

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

# create directory to store temporary files
os.makedirs("data/temp/dtm/", exist_ok=True)
os.makedirs("data/rasters/", exist_ok=True)

feedback = QgsProcessingFeedback()

# convert bathymetry raster to points
params = {
    "INPUT_RASTER": "data/raw/rasters/bathymetry.asc",
    "RASTER_BAND": 1,
    "FIELD_NAME": "VALUE",
    "OUTPUT": "data/temp/dtm/bathymetry_pts_temp.shp"
}
processing.run("native:pixelstopoints", params, feedback=feedback)

# assign projection
params = {
    "INPUT": "data/temp/dtm/bathymetry_pts_temp.shp",
    "CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
    "OUTPUT": "data/temp/dtm/bathymetry_pts_wgs84.shp"
}
processing.run("native:assignprojection", params, feedback=feedback)

# reproject points from WGS84 to OSGB 1936
params = {
    "INPUT": "data/temp/dtm/bathymetry_pts_wgs84.shp",
    "TARGET_CRS": QgsCoordinateReferenceSystem("EPSG:27700"),
    "OUTPUT": "data/temp/dtm/bathymetry_pts_osgb.shp"
}
processing.run("native:reprojectlayer", params, feedback=feedback)

# clip points to study area
params = {
    "INPUT": "data/temp/dtm/bathymetry_pts_osgb.shp",
    "MASK": "data/data.gpkg|layername=study_area_water",
    "OUTPUT": "data/temp/dtm/bathymetry_pts.shp"
}
processing.run("gdal:clipvectorbypolygon", params, feedback=feedback)

# define data sources
basePath = "data/data.gpkg|layername="
extentLayer = basePath + "study_area"
spotheightLayer = basePath + "os_terrain50_spotheight"
contourLayer = basePath + "os_terrain50_contourline"
boundaryLayer = basePath + "os_terrain50_landwaterboundary"
bathymetryLayer = "data/temp/dtm/bathymetry_pts.shp"

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
    "OUTPUT": "data/temp/dtm/terrain_temp.tif",
    "TRIANGULATION": "data/temp/dtm/terrain_tin.shp"
}
processing.run("qgis:tininterpolation", params, feedback=feedback)

# clip to study area
params = {
    "INPUT": "data/temp/dtm/terrain_temp.tif",
    "MASK": extentLayer,
    "OUTPUT": "data/rasters/terrain.tif"
}
processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

# clip DTM to N4
params = {
    "INPUT": "data/rasters/terrain.tif",
    "MASK": "data/data.gpkg|layername=sectoral_marine_plan_N4",
    "OUTPUT": "data/rasters/terrain_N4.tif"
}
processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

# ######################################################################
# call exitQgis() to remove the provider and layer registries from memory
qgs.exitQgis()

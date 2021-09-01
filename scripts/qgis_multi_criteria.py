"""Multi criteria analysis

Classes
-------
Population:
1) 0 < x <= 2.5e-06 -> 1
2) 2.5e-06 < x <= 5e-06 -> 0.8
3) 5e-06 < x <= 7.5e-06 -> 0.6
4) 7.5e-06 < x <= 1e-05 -> 0.4
5) 1e-05 < x <= 1.25e-05 -> 0.2
6) 1.25e-05 < x <= 1.5e-05 -> 0

Distance to shore:
1) 0 < x <= 5000 -> 0
2) 5000 < x <= 10000 -> 0.2
3) 10000 < x <= 15000 -> 0.4
4) 15000 < x <= 20000 -> 0.6
5) 20000 < x <= 25000 -> 0.8
6) 25000 < x <= 30000 -> 1

Distance from scenic areas:
1) 0 < x <= 7500 -> 0
2) 7500 < x <= 15000 -> 0.2
3) 15000 < x <= 22500 -> 0.4
4) 22500 < x <= 30000 -> 0.6
5) 30000 < x <= 37500 -> 0.8
6) 37500 < x <= 45000 -> 1

range boundaries: min < value <= max
"""

# set paths to QGIS libraries
# may be necessary if using Windows
# exec(open("scripts/set_sys_paths.py").read())

# import libraries
from qgis.core import QgsApplication, QgsProcessingFeedback, QgsProperty

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

feedback = QgsProcessingFeedback()

# create directory to store files
os.makedirs("data/temp/mca", exist_ok=True)

# interpolate population data
params = {
    "INPUT": "data/data.gpkg|layername=census_centroids",
    "RADIUS": 35000,
    "PIXEL_SIZE": 10,
    "WEIGHT_FIELD": "All people",
    "KERNEL": 0,
    "DECAY": 0,
    "OUTPUT_VALUE": 1,
    "OUTPUT": "data/temp/mca/population_heatmap.tif"
}
processing.run(
    "qgis:heatmapkerneldensityestimation", params, feedback=feedback
)

# clip to study area
params = {
    "INPUT": "data/temp/mca/population_heatmap.tif",
    "MASK": "data/data.gpkg|layername=study_area_water",
    "SOURCE_CRS": None,
    "TARGET_CRS": None,
    "NODATA": None,
    "ALPHA_BAND": False,
    "CROP_TO_CUTLINE": True,
    "KEEP_RESOLUTION": False,
    "SET_RESOLUTION": False,
    "X_RESOLUTION": None,
    "Y_RESOLUTION": None,
    "MULTITHREADING": False,
    "DATA_TYPE": 0,
    "OUTPUT": "data/temp/mca/population_heatmap_clipped.tif"
}
processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

# reclassify
tbl = [
    0, 2.5e-06, 1, 2.5e-06, 5e-06, 0.8, 5e-06, 7.5e-06, 0.6,
    7.5e-06, 1e-05, 0.4, 1e-05, 1.25e-05, 0.2, 1.25e-05, 1.5e-05, 0
]
params = {
    "INPUT_RASTER": "data/temp/mca/population_heatmap_clipped.tif",
    "RASTER_BAND": 1,
    "TABLE": tbl,
    "NO_DATA": -9999,
    "RANGE_BOUNDARIES": 0,
    "NODATA_FOR_MISSING": False,
    "DATA_TYPE": 5,
    "OUTPUT": "data/rasters/population_heatmap.tif"
}
processing.run("native:reclassifybytable", params, feedback=feedback)

# ######################################################################
# distance to shore buffers - six 5 km rings
params = {
    "INPUT": "data/data.gpkg|layername=os_terrain50_lowwater",
    "RINGS": 6,
    "DISTANCE": 5000,
    "OUTPUT": "data/temp/mca/dist_to_shore_buffer.shp"
}
processing.run("native:multiringconstantbuffer", params, feedback=feedback)

# dissolve
params = {
    "INPUT": "data/temp/mca/dist_to_shore_buffer.shp",
    "FIELD": ["ringId", "distance"],
    "OUTPUT": "data/temp/mca/dist_to_shore_dissolved.shp"
}
processing.run("native:dissolve", params, feedback=feedback)

# order fields by expression (distance)
params = {
    "INPUT": "data/temp/mca/dist_to_shore_dissolved.shp",
    "EXPRESSION": "\"distance\"",
    "ASCENDING": False,
    "NULLS_FIRST": False,
    "OUTPUT": "data/temp/mca/dist_to_shore_sort.shp"
}
processing.run("native:orderbyexpression", params, feedback=feedback)

# rasterise
ext = (
    "93951.519500000,147902.827900000,931331.420600000,980507.702700000" +
    " [EPSG:27700]"
)
params = {
    "INPUT": "data/temp/mca/dist_to_shore_sort.shp",
    "FIELD": "distance",
    "BURN": None,
    "USE_Z": False,
    "UNITS": 1,
    "WIDTH": 10,
    "HEIGHT": 10,
    "EXTENT": ext,
    "NODATA": None,
    "DATA_TYPE": 5,
    "INIT": None,
    "INVERT": False,
    "OUTPUT": "data/temp/mca/dist_to_shore_rasterise.tif"
}
processing.run("gdal:rasterize", params, feedback=feedback)

# clip
params = {
    "INPUT": "data/temp/mca/dist_to_shore_rasterise.tif",
    "MASK": "data/data.gpkg|layername=study_area_water",
    "SOURCE_CRS": None,
    "TARGET_CRS": None,
    "NODATA": -9999,
    "ALPHA_BAND": False,
    "CROP_TO_CUTLINE": False,
    "KEEP_RESOLUTION": False,
    "SET_RESOLUTION": False,
    "X_RESOLUTION": None,
    "Y_RESOLUTION": None,
    "MULTITHREADING": False,
    "DATA_TYPE": 0,
    "OUTPUT": "data/temp/mca/dist_to_shore_clipped.tif"
}
processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

# reclassify
tbl = [
    0, 5000, 0, 5000, 10000, 0.2, 10000, 15000, 0.4, 15000, 20000, 0.6,
    20000, 25000, 0.8, 25000, 30000, 1
]
params = {
    "INPUT_RASTER": "data/temp/mca/dist_to_shore_clipped.tif",
    "RASTER_BAND": 1,
    "TABLE": tbl,
    "NO_DATA": -9999,
    "RANGE_BOUNDARIES": 0,
    "NODATA_FOR_MISSING": False,
    "DATA_TYPE": 5,
    "OUTPUT": "data/rasters/distance_to_shore.tif"
}
processing.run("native:reclassifybytable", params, feedback=feedback)

# ######################################################################
# distance to scenic areas
params = {
    "INPUT": "data/data.gpkg|layername=national_scenic_areas",
    "RINGS": 9,
    "DISTANCE": 5000,
    "OUTPUT": "data/temp/mca/dist_from_nsa_buffer.shp"
}
processing.run("native:multiringconstantbuffer", params, feedback=feedback)

# rasterise
ext = (
    "93951.519500000,147902.827900000,931331.420600000,980507.702700000" +
    " [EPSG:27700]"
)
params = {
    "INPUT": "data/temp/mca/dist_from_nsa_buffer.shp",
    "FIELD": "distance",
    "BURN": None,
    "USE_Z": False,
    "UNITS": 1,
    "WIDTH": 10,
    "HEIGHT": 10,
    "EXTENT": ext,
    "NODATA": None,
    "DATA_TYPE": 5,
    "INIT": None,
    "INVERT": False,
    "OUTPUT": "data/temp/mca/dist_from_nsa_rasterise.tif"
}
processing.run("gdal:rasterize", params, feedback=feedback)

# clip
params = {
    "INPUT": "data/temp/mca/dist_from_nsa_rasterise.tif",
    "MASK": "data/data.gpkg|layername=study_area_water",
    "SOURCE_CRS": None,
    "TARGET_CRS": None,
    "NODATA": -9999,
    "ALPHA_BAND": False,
    "CROP_TO_CUTLINE": False,
    "KEEP_RESOLUTION": False,
    "SET_RESOLUTION": False,
    "X_RESOLUTION": None,
    "Y_RESOLUTION": None,
    "MULTITHREADING": False,
    "DATA_TYPE": 0,
    "OUTPUT": "data/temp/mca/dist_from_nsa_clipped.tif"
}
processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

# reclassify
tbl = [
    0, 7500, 0, 7500, 15000, 0.2, 15000, 22500, 0.4, 22500, 30000, 0.6,
    30000, 37500, 0.8, 37500, 45000, 1
]
params = {
    "INPUT_RASTER": "data/temp/mca/dist_from_nsa_clipped.tif",
    "RASTER_BAND": 1,
    "TABLE": tbl,
    "NO_DATA": -9999,
    "RANGE_BOUNDARIES": 0,
    "NODATA_FOR_MISSING": False,
    "DATA_TYPE": 5,
    "OUTPUT": "data/rasters/distance_from_nsa.tif"
}
processing.run("native:reclassifybytable", params, feedback=feedback)

# ######################################################################
# marine species
# extract entries with species count attribute
params = {
    "INPUT": "data/data.gpkg|layername=gems_species",
    "FIELD": "SPCOUNT",
    "OPERATOR": 3,
    "VALUE": "0",
    "OUTPUT": "data/temp/mca/gems_species_count.shp"
}
processing.run("native:extractbyattribute", params, feedback=feedback)

# create buffers weighted by species count
params = {
    "INPUT": "data/temp/mca/gems_species_count.shp",
    "DISTANCE": QgsProperty.fromExpression("\"SPCOUNT\""),
    "SEGMENTS": 5,
    "END_CAP_STYLE": 0,
    "JOIN_STYLE": 0,
    "MITER_LIMIT": 2,
    "DISSOLVE": False,
    "OUTPUT": "data/temp/mca/gems_species_count_buffer.shp"
}
processing.run("native:buffer", params, feedback=feedback)

# create 1 km buffer exclusion zones
params = {
    "INPUT": "data/temp/mca/gems_species_count_buffer.shp",
    "DISTANCE": 1000,
    "SEGMENTS": 5,
    "END_CAP_STYLE": 0,
    "JOIN_STYLE": 0,
    "MITER_LIMIT": 2,
    "DISSOLVE": False,
    "OUTPUT": "data/temp/mca/gems_species_buffer.shp"
}
processing.run("native:buffer", params, feedback=feedback)

# ######################################################################
# cumulative raster
exp = (
    "( \"distance_to_shore@1\" + \"distance_from_nsa@1\" + " +
    "\"population_heatmap@1\" )  / 3"
)
params = {
    "EXPRESSION": exp,
    "LAYERS": ["data/rasters/population_heatmap.tif"],
    "CELLSIZE": None,
    "EXTENT": None,
    "CRS": None,
    "OUTPUT": "data/rasters/multicriteria.tif"
}
processing.run("qgis:rastercalculator", params, feedback=feedback)

# ######################################################################
# call exitQgis() to remove the provider and layer registries from memory
qgs.exitQgis()

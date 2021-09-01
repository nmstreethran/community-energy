"""Viewshed analysis

Spacing
-------
25 turbines: 2880 m
50 turbines: 2000 m
75 turbines: 1625 m
100 turbines: 1400 m

Classes
-------
100 turbines:
1) 0 < x <= 4250 -> 0
2) 4250 < x <= 8500 -> 0.2
3) 8500 < x <= 12750 -> 0.4
4) 12750 < x <= 17000 -> 0.6
5) 17000 < x <= 21250 -> 0.8
6) 21250 < x <= 25500 -> 1

75 turbines:
1) 0 < x <= 3187.5 -> 0
2) 3187.5 < x <= 6375 -> 0.2
3) 6375 < x <= 9562.5 -> 0.4
4) 9562.5 < x <= 12750 -> 0.6
5) 12750 < x <= 15937.5 -> 0.8
6) 15937.5 < x <= 19125 -> 1

50 turbines:
1) 0 < x <= 2125 -> 0
2) 2125 < x <= 4250 -> 0.2
3) 4250 < x <= 6375 -> 0.4
4) 6375 < x <= 8500 -> 0.6
5) 8500 < x <= 10625 -> 0.8
6) 10625 < x <= 12750 -> 1

25 turbines:
1) 0 < x <= 1062.5 -> 0
2) 1062.5 < x <= 2125 -> 0.2
3) 2125 < x <= 3187.5 -> 0.4
4) 3187.5 < x <= 4250 -> 0.6
5) 4250 < x <= 5312.5 -> 0.8
6) 5312.5 < x <= 6375 -> 1

range boundaries: min < value <= max
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
# import required Python libraries
import os
import glob
import geopandas as gpd

feedback = QgsProcessingFeedback()

# create directory to store files
os.makedirs("data/temp/viewshed", exist_ok=True)

# generate turbine distribution in N4
n4 = "data/data.gpkg|layername=sectoral_marine_plan_N4"
turbDist = [(25, 2880), (50, 2000), (75, 1625), (100, 1400)]

for n, d in turbDist:
    distLayer = (
        "ogr:dbname=\'data/temp/viewshed/turbine_dist_temp.gpkg\' table=\"" +
        str(n) + "_turbines\" (geom)"
    )
    params = {
        "EXTENT": n4,
        "SPACING": d,
        "INSET": 0,
        "RANDOMIZE": False,
        "IS_SPACING": True,
        "CRS": QgsCoordinateReferenceSystem("EPSG:27700"),
        "OUTPUT": distLayer
    }
    processing.run("qgis:regularpoints", params, feedback=feedback)
    outLayer = (
        "data/temp/viewshed/turbine_dist_temp.gpkg|layername=" + str(n) +
        "_turbines"
    )
    distLayer = (
        "ogr:dbname=\'data/temp/viewshed/turbine_dist.gpkg\' table=\"" +
        str(n) + "_turbines\" (geom)"
    )
    params = {
        "INPUT": outLayer,
        "OVERLAY": n4,
        "OUTPUT": distLayer
    }
    processing.run("native:intersection", params, feedback=feedback)

# viewshed for each scenario
scenarios = [
    (100, 180), (75, 180), (50, 180), (25, 180), (25, 200), (25, 160)
]

for n, h in scenarios:
    # create directory to store files
    os.makedirs(
        "data/temp/viewshed/" + str(n) + "t_" + str(h) + "m", exist_ok=True
    )
    nLayer = gpd.read_file(
        "data/data.gpkg", layer="scenario_"+str(n)+"_turbines"
    )
    for i in range(len(nLayer)):
        obs = (
            str(nLayer["geometry"][i][0].x) + "," +
            str(nLayer["geometry"][i][0].y) + " [EPSG:27700]"
        )
        outFile = (
            "data/temp/viewshed" + str(n) + "t_" + str(h) + "m/" + str(i) +
            ".tif"
        )
        params = {
            "INPUT": "data/rasters/terrain.tif",
            "BAND": 1,
            "OBSERVER": obs,
            "OBSERVER_HEIGHT": h + 50,
            "TARGET_HEIGHT": 1.65,
            "MAX_DISTANCE": 45000,
            "OUTPUT": outFile
        }
        processing.run("gdal:viewshed", params, feedback=feedback)

# obtain cumulative viewsheds
# this was done using the QGIS interface
# code still being worked on
rList = list(range(1, 100))
expr = "\"0@1\""
for r in rList:
    expr = expr + " + \"" + str(r) + "@1\""
params = {
    "EXPRESSION": expr,
    "LAYERS": ["100t_180m/0.tif"],
    "OUTPUT": "100t_180m_temp.tif"
}
processing.run("qgis:rastercalculator", params, feedback=feedback)

# clip viewshed raster to study area
folderList = glob.glob("data/temp/viewshed/*m")
for fld in folderList:
    params = {
        "INPUT": fld + "_temp.tif",
        "MASK": "data/data.gpkg|layername=study_area",
        "SOURCE_CRS": None,
        "TARGET_CRS": None,
        "NODATA": None,
        "ALPHA_BAND": False,
        "CROP_TO_CUTLINE": False,
        "KEEP_RESOLUTION": False,
        "SET_RESOLUTION": False,
        "X_RESOLUTION": None,
        "Y_RESOLUTION": None,
        "MULTITHREADING": False,
        "DATA_TYPE": 0,
        "OUTPUT": fld + ".tif"
    }
    processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

    # clip to land area
    params = {
        "INPUT": fld + ".tif",
        "MASK": "data/data.gpkg|layername=os_bdline_westernisles",
        "SOURCE_CRS": None,
        "TARGET_CRS": None,
        "NODATA": None,
        "ALPHA_BAND": False,
        "CROP_TO_CUTLINE": False,
        "KEEP_RESOLUTION": False,
        "SET_RESOLUTION": False,
        "X_RESOLUTION": None,
        "Y_RESOLUTION": None,
        "MULTITHREADING": False,
        "DATA_TYPE": 0,
        "OUTPUT": fld + "_clip.tif"
    }
    processing.run("gdal:cliprasterbymasklayer", params, feedback=feedback)

# reclassify and normalise viewshed raster
tbl = [
    0, 1062.5, 0, 1062.5, 2125, 0.2, 2125, 3187.5, 0.4, 3187.5, 4250, 0.6,
    4250, 5312.5, 0.8, 5312.5, 6375, 1
]
inRaster = "data/temp/viewshed/25t_180m_clip.tif"
outRaster = "data/rasters/viewshed_25t_180m.tif"

params = {
    "INPUT_RASTER": inRaster,
    "RASTER_BAND": 1,
    "TABLE": tbl,
    "NO_DATA": -9999,
    "RANGE_BOUNDARIES": 0,
    "NODATA_FOR_MISSING": False,
    "DATA_TYPE": 5,
    "OUTPUT": outRaster
}
processing.run("native:reclassifybytable", params, feedback=feedback)

# generate viewpoint centroids
params = {
    "INPUT": "data/data.gpkg|layername=viewpoints",
    "ALL_PARTS": False,
    "OUTPUT": "data/temp/viewshed/viewpoint_centroids.shp"
}
processing.run("native:centroids", params, feedback=feedback)

# generate 100 m buffer
params = {
    "INPUT": "data/temp/viewshed/viewpoint_centroids.shp",
    "RINGS": 1,
    "DISTANCE": 100,
    "OUTPUT": "data/temp/viewshed/viewpoint_buffer.shp"
}
processing.run("native:multiringconstantbuffer", params, feedback=feedback)

# generate zonal statistics for each viewshed raster
outLayer = (
    "ogr:dbname=\'data/data.gpkg\' table=\"" +
    "zonalstats_25t_180m\" (geom)"
)
params = {
    "INPUT": "data/temp/viewshed/viewpoint_buffer.shp",
    "INPUT_RASTER": "data/rasters/viewshed_25t_180m.tif",
    "RASTER_BAND": 1,
    "COLUMN_PREFIX": "zs_",
    "STATISTICS": [0, 1, 2, 4, 5, 6],
    "OUTPUT": outLayer
}
processing.run("native:zonalstatisticsfb", params, feedback=feedback)

# generate zonal statistics at each viewpoint for digital terrain model
# save as layers in data/data.gpkg

# ######################################################################
# call exitQgis() to remove the provider and layer registries from memory
qgs.exitQgis()

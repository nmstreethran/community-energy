"""Standalone QGIS Python script template

"""

# set paths to QGIS libraries
# may be necessary if using Windows
# exec(open("scripts/set_sys_paths.py").read())

# import libraries
from qgis.core import (
    QgsApplication, QgsProject, QgsVectorLayer, QgsProcessingFeedback
)
import os

# create a reference to the QgsApplication
# setting the second argument to False disables the GUI
qgs = QgsApplication([], True)

# load providers
qgs.initQgis()

# set-up QGIS plugin installer
import pyplugin_installer
pyplugin_installer.instance().fetchAvailablePlugins(False)
# view available plugins
pyplugin_installer.installer_data.plugins.all().keys()
# install required plugins
pyplugin_installer.instance().installPlugin("pluginName")

# import processing libraries
from qgis import processing
from processing.core.Processing import Processing
Processing.initialize()

# print the settings
print(qgs.showSettings())

# check the current working directory
os.getcwd()
# change the directory if it is not the current project
# os.chdir()

# get the project instance
project = QgsProject.instance()

# load an existing project
project.read("project.qgz")
# or create a new project
# project.write("project.qgz")

# ###################################################################
# BEGIN ANALYSIS

feedback = QgsProcessingFeedback()

# view an algorithm's specifications
processing.algorithmHelp("qgis:tininterpolation")

# specify the input data


def addVectorLayer(layerPath, layerTitle):
    layer = layerPath
    layer = QgsVectorLayer(layer, layerTitle, "ogr")
    if not layer.isValid():
        print("Layer invalid! " + str(layer))
    else:
        QgsProject.instance().addMapLayer(layer)


addVectorLayer("layer.shp")
addVectorLayer("data.gpkg|layername=layer")

# END ANALYSIS
# ###################################################################

# save the project
project.write()

# call exitQgis() to remove the provider and layer registries from memory
qgs.exitQgis()

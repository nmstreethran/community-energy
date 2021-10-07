# Offshore Wind Community Impacts

GIS project on mapping the impacts of a proposed offshore wind development plan on Isle of Lewis communities

Originally completed as part of my dissertation at the University of Aberdeen

## Set-up

To execute scripts in your own Python environment, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html); choose the Python 3.9 installer.

Create and activate a virtual environment with all required packages (including QGIS):

```sh
conda create --name owci --channel conda-forge python=3.9 geopandas requests qgis
conda activate owci
```

Install these additional requirements:

- if using Windows:

  ```sh
  conda install --channel conda-forge 7zip
  ```

- to run Jupyter Notebooks:

  ```sh
  conda install --channel conda-forge matplotlib rioxarray jupyterlab
  ```

To launch the QGIS GUI using this environment, run `qgis`. The scripts can then be copied and pasted into QGIS' Python console.

Note: Bathymetry data must be downloaded manually from the EMODnet Bathymetry portal.

## Data

Name | Source | Format | Version | Coverage | CRS
----- | --- | -- | -- | --- | --
Sectoral Marine Plan for Offshore Wind Energy Draft Plan Options | [Marine Scotland](https://marine.gov.scot/data/sectoral-marine-plan-offshore-wind-energy-draft-plan-options-gis-files) | Shapefile | 01/2020 | Scotland | EPSG:4326
Scheduled Monuments | [Historic Environment Scotland](https://portal.historicenvironment.scot/downloads/scheduledmonuments) | Shapefile | 08/2020 | Scotland | EPSG:27700
1:250 000 Scale Colour Raster™ | [Ordnance Survey](https://www.ordnancesurvey.co.uk/business-government/products/250k-raster) | TIFF-LZW | 06/2021 | Great Britain | EPSG:27700
Boundary-Line™ | [Ordnance Survey](https://www.ordnancesurvey.co.uk/business-government/products/boundaryline) | GeoPackage | 05/2021 | Great Britain | EPSG:27700
OS Terrain® 50 - 10 m contours | [Ordnance Survey](https://www.ordnancesurvey.co.uk/business-government/products/terrain-50) | GeoPackage | 07/2020 | Great Britain | EPSG:27700
OS Open Names | [Ordnance Survey](https://www.ordnancesurvey.co.uk/business-government/products/open-map-names) | CSV | 04/2021 | Great Britain | EPSG:27700
OS British National Grids | [Ordnance Survey](https://github.com/OrdnanceSurvey/OS-British-National-Grids) | GeoPackage | 01/2021 | Great Britain | EPSG:27700
EMODnet Digital Bathymetry (DTM 2020) | [EMODnet](https://www.emodnet-bathymetry.eu/) | ASCII | 2020 | Area of Interest | EPSG:4326
GeMS - Scottish Priority Marine Features (PMF) | [NatureScot](https://gateway.snh.gov.uk/natural-spaces/datasets/GEMS-PMF) | File Geodatabase | 2021-02 | Scotland | EPSG:4326
Marine Consultation Areas | [NatureScot](https://gateway.snh.gov.uk/natural-spaces/datasets/MCA) | Shapefile | 2012-02 | Scotland | EPSG:27700
National Scenic Areas | [Scottish Government](https://www.spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/13396739-7602-4428-85fd-95a5d7e208a1) | Shapefile | 1998 | Scotland | EPSG:27700
2011 Output Area Boundaries - Extent of the Realm | [National Records of Scotland](https://www.nrscotland.gov.uk/statistics-and-data/geography/our-products/census-datasets/2011-census/2011-boundaries) | Shapefile | 2013-09 | Scotland | EPSG:27700
2011 Output Area - Population Weighted Centroids | [National Records of Scotland](https://www.nrscotland.gov.uk/statistics-and-data/geography/our-products/census-datasets/2011-census/2011-boundaries) | Shapefile | 2013-09 | Scotland | EPSG:27700
2011 census table data: Output Area 2011 | [National Records of Scotland](https://www.scotlandscensus.gov.uk/documents/2011-census-table-data-output-area-2011/) | CSV | 2021-04 | Scotland
Community Council Boundaries | [Improvement Service](https://data.spatialhub.scot/dataset/community_council_boundaries-is) | Shapefile | 2021-07 | Scotland | EPSG:27700

## Licence

(C) 2021 Nithiya Streethran

This work is licenced under the [GNU General Public License v3.0 or later (GPL-3.0-or-later)](https://www.gnu.org/licenses/gpl-3.0.html).

This project uses public sector information licenced under the [Open Government Licence (OGL) v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

- Contains Ordnance Survey data, Royal Mail, National Statistics, Scottish Government, Marine Scotland, and National Records of Scotland data. (C) Crown copyright and database right 2021.
- Contains Historic Environment Scotland data. (C) Historic Environment Scotland - Scottish Charity No. SC045925 2021.
- Contains Scottish Natural Heritage information. (C) NatureScot 2021.
- Contains Scottish local authority data from the Spatial Hub. (C) Improvement Service 2021.

Bathymetry data used in this project was made available by the EMODnet Bathymetry project, funded by the European Commission Directorate General for Maritime Affairs and Fisheries. The data originators are the United Kingdom Hydrographic Office (UKHO), OceanWise Limited, and the General Bathymetric Chart of the Oceans (GEBCO).

All data used in this project are not to be used for navigation or for any other purpose relating to safety at sea.

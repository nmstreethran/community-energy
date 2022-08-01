# Mapping the impacts of a proposed offshore wind development plan on Isle of Lewis communities

[![DOI](badges/ZENODO_poster.svg)](https://doi.org/10.5281/zenodo.6847982)
[![Report (PDF)](badges/REPORT.svg)](https://media.githubusercontent.com/media/nmstreethran/community-energy/main/docs/report.pdf)

GIS project on mapping the impacts of a proposed offshore wind development plan on Isle of Lewis communities

by Nithiya Streethran (nmstreethran@gmail.com)

Originally completed as part of my MSc dissertation at the University of Aberdeen between May and August 2021

## Set-up

To execute scripts in your own Python environment, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html); choose the Python 3.9 installer.

Create and activate a virtual environment with all required packages (including QGIS):

```sh
conda env create
conda activate community-energy
```

To launch the QGIS GUI using this environment, run `qgis`. The scripts can then be copied and pasted into QGIS' Python console.

Note: Bathymetry data must be downloaded manually from the EMODnet Bathymetry portal.

## Data

Name | Source | Format | Version | Coverage | CRS (EPSG) | Metadata
----- | --- | -- | -- | --- | -- | --
Sectoral Marine Plan for Offshore Wind Energy Draft Plan Options | [Marine Scotland] | Shapefile | 01/2020 | Scotland | 4326 | [[1]]
Scheduled Monuments | [Historic Environment Scotland] | Shapefile | 08/2020 | Scotland | 27700 | [[2]]
1:250 000 Scale Colour Raster™ | [Ordnance Survey][OS250k] | TIFF-LZW | 06/2021 | Great Britain | 27700
Boundary-Line™ | [Ordnance Survey][OSBdL] | GeoPackage | 10/2021 | Great Britain | 27700
OS Terrain® 50 - 10 m contours | [Ordnance Survey][OST50] | GeoPackage | 07/2021 | Great Britain | 27700
OS Open Names | [Ordnance Survey][OSON] | CSV | 10/2021 | Great Britain | 27700
OS British National Grids | [Ordnance Survey][OSBNG] | GeoPackage | 01/2021 | Great Britain | 27700
EMODnet Digital Bathymetry (DTM 2020) | [EMODnet] | ASCII | 2020 | Area of Interest | 4326
GeMS - Scottish Priority Marine Features (PMF) | [NatureScot][NSGeMS] | File Geodatabase | 02/2021 | Scotland | 4326 | [[3]]
Marine Consultation Areas | [NatureScot][NSMCA] | Shapefile | 02/2012 | Scotland | 27700 | [[4]]
National Scenic Areas | [Scottish Government][5] | Shapefile | 1998 | Scotland | 27700 | [[5]]
2011 Output Area Boundaries - Extent of the Realm | [National Records of Scotland][NRSOAB] | GML | 09/2013 | Scotland | 27700 | [[6]]
2011 Output Area - Population Weighted Centroids | [National Records of Scotland][NRSOAB] | GML | 09/2013 | Scotland | 27700 | [[7]]
2011 census table data: Output Area 2011 | [National Records of Scotland][NRSCT] | CSV | 04/2021 | Scotland
Community Council Boundaries | [Improvement Service] | Shapefile | 11/2021 | Scotland | 27700 | [[8]]

### Clipped data

- layers in `boundaries.gpkg`
  - Sectoral Marine Plan options: `sectoral_marine_plan`
  - Sectoral Marine Plan option N4: `sectoral_marine_plan_N4`
  - 15 km study area buffer around N4: `study_area`
  - OS Boundary-Line
    - Scottish Constituencies: `os_bdline_scotland_const`
    - Scotland: `os_bdline_scotland`
    - Western Isles: `os_bdline_westernisles_const`
  - Community council boundaries: `community_council`
- layers in `context.gpkg`
  - British National Grids (various resolutions, GB coverage): `100km_grid`, `50km_grid`, `20km_grid`, `10km_grid`, `5km_grid`, `1km_grid`
  - OS Open Names, covering NA8 and NB: `os_opennames`

## Jupyter notebooks

WIP

&nbsp; | Output
-- | --
OS Downloads API | [![View Jupyter Notebook](badges/NOTEBOOK.svg)](https://nbviewer.org/gist/nmstreethran/c4379db1063b0895606f361a8abbf839/os_downloads_api.ipynb)
Study area definition | [![View Jupyter Notebook](badges/NOTEBOOK.svg)](https://nbviewer.org/gist/nmstreethran/c4379db1063b0895606f361a8abbf839/study_area_def.ipynb)
Context | [![View Jupyter Notebook](badges/NOTEBOOK.svg)](https://nbviewer.org/gist/nmstreethran/c4379db1063b0895606f361a8abbf839/context.ipynb)

## Maps

WIP

[![2D Web Map on ArcGIS Online](badges/2D_WEB_MAP.svg)](https://www.arcgis.com/apps/webappviewer/index.html?id=5da0279a967843b2836c22119e3ea572)
[![3D Web Scene on ArcGIS Online](badges/3D_WEB_SCENE.svg)](https://www.arcgis.com/apps/webappviewer3d/index.html?id=6199462acc17455c888b7940508d272a)

## Licence

(C) 2021-2022 Nithiya Streethran

This work is licenced under the [GNU General Public License v3.0 or later (GPL-3.0-or-later)](https://www.gnu.org/licenses/gpl-3.0.html).

This project uses public sector information licenced under the [Open Government Licence (OGL) v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

- Contains Ordnance Survey data, Royal Mail, National Statistics, Scottish Government, Marine Scotland, and National Records of Scotland data. (C) Crown copyright and database right 2021.
- Contains Historic Environment Scotland data. (C) Historic Environment Scotland - Scottish Charity No. SC045925 2021.
- Contains Scottish Natural Heritage information. (C) NatureScot 2021.
- Contains Scottish local authority data from the Spatial Hub. (C) Improvement Service 2021.

Bathymetry data used in this project was made available by the EMODnet Bathymetry project, funded by the European Commission Directorate General for Maritime Affairs and Fisheries. The data originators are the United Kingdom Hydrographic Office (UKHO), OceanWise Limited, and the General Bathymetric Chart of the Oceans (GEBCO).

All data used in this project are not to be used for navigation or for any other purpose relating to safety at sea.

Documentation is licenced under a [Creative Commons Attribution 4.0 International (CC-BY-4.0) License](https://creativecommons.org/licenses/by/4.0/).

Badges were generated using [Shields.io](https://shields.io/).

[Marine Scotland]: https://marine.gov.scot/data/sectoral-marine-plan-offshore-wind-energy-draft-plan-options-gis-files
[Historic Environment Scotland]: https://portal.historicenvironment.scot/downloads/scheduledmonuments
[OS250k]: https://www.ordnancesurvey.co.uk/business-government/products/250k-raster
[OSBdL]: https://www.ordnancesurvey.co.uk/business-government/products/boundaryline
[OST50]: https://www.ordnancesurvey.co.uk/business-government/products/terrain-50
[OSON]: https://www.ordnancesurvey.co.uk/business-government/products/open-map-names
[OSBNG]: https://github.com/OrdnanceSurvey/OS-British-National-Grids
[EMODnet]: https://www.emodnet-bathymetry.eu/
[NSGeMS]: https://gateway.snh.gov.uk/natural-spaces/datasets/GEMS-PMF
[NSMCA]: https://gateway.snh.gov.uk/natural-spaces/datasets/MCA
[NRSOAB]: https://www.nrscotland.gov.uk/statistics-and-data/geography/our-products/census-datasets/2011-census/2011-boundaries
[NRSCT]: https://www.scotlandscensus.gov.uk/documents/2011-census-table-data-output-area-2011/
[Improvement Service]: https://data.spatialhub.scot/dataset/community_council_boundaries-is
[1]: https://spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/Marine_Scotland_FishDAC_12263
[2]: https://spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/756ec396-b6f9-4efe-8309-2dad95ffef68
[3]: https://spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/3bcb9784-6c3c-410a-9096-4d7777454ac5
[4]: https://spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/7C6A9F67-7581-404B-AE59-8DE523291550
[5]: https://spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/13396739-7602-4428-85fd-95a5d7e208a1
[6]: https://spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/e8544752-8d8e-4be4-8fad-68e7e70a90b8
[7]: https://spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/9d977a73-7884-4870-ae76-afccf8e6fae8
[8]: https://spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/83b038d4-1d33-4acf-83ea-e5dcc510a034

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

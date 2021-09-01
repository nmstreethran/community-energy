"""Clip all datasets

- projection used is EPSG:27700
- study area is 15 km buffer around SMP option N4
- reproject if necessary
- additional processing
- also create viewpoints
"""

# import libraries
import glob
import fiona
import geopandas as gpd
import pandas as pd

# define path to GeoPackage to store vector data
gpkgPath = "data/input.gpkg"

# ###########################################################
# Sectoral Marine Plan (SMP) options
data = gpd.read_file(glob.glob("data/raw/marine/smp/*.shp")[0])

list(data)
# ['name', 'copyright', 'date', 'comments', 'geometry']

# keep only N4
data = data.loc[data["name"] == "N4"]

# reproject
if data.crs != 27700:
    data = data.to_crs("epsg:27700")
    print("Data reprojected to EPSG:27700")

# save as a GeoPackage layer
data.to_file(gpkgPath, layer="sectoral_marine_plan_N4", driver="GPKG")
print("Layer 'sectoral_marine_plan_N4' saved!")

# ###########################################################
# buffer SMP polygon to get study area
area = gpd.GeoDataFrame(geometry=data.buffer(15000), crs="EPSG:27700")

area["name"] = "Study area"
area["description"] = "15 km buffer around Sectoral Marine Plan option N4"

# save as a GeoPackage layer
area.to_file(gpkgPath, layer="study_area", driver="GPKG")
print("Layer 'study_area' saved!")

# ###########################################################
# OS British National Grid tiles
layers = fiona.listlayers(
    glob.glob("data/raw/administrative/os_bng/*.gpkg")[0]
)

# get all tiles within the buffer
for res in layers:
    data = gpd.read_file(
        glob.glob("data/raw/administrative/os_bng/*.gpkg")[0],
        layer=res,
        mask=area
    )
    data.to_file(gpkgPath, layer="os_bng_"+res, driver="GPKG")
    print("Layer 'os_bng_" + res + "' saved!")

# ###########################################################
# OS BoundaryLine
fiona.listlayers(glob.glob("data/raw/administrative/os_bdline/*/*.gpkg")[0])
# ['boundary_line_ceremonial_counties', 'boundary_line_historic_counties',
# 'community_ward', 'country_region', 'county', 'county_electoral_division',
# 'district_borough_unitary', 'district_borough_unitary_ward',
# 'english_region', 'greater_london_const', 'high_water',
# 'historic_european_region', 'parish', 'polling_districts_england',
# 'scotland_and_wales_const', 'scotland_and_wales_region',
# 'unitary_electoral_division', 'westminster_const']

# read boundary line data
bound = gpd.read_file(
    glob.glob("data/raw/administrative/os_bdline/*/*.gpkg")[0],
    layer="scotland_and_wales_const",
    bbox=area
)

# save as a GeoPackage layer
bound.to_file(gpkgPath, layer="os_bdline_westernisles", driver="GPKG")
print("Layer 'os_bdline_westernisles' saved!")

# save Scotland's boundary
data = gpd.read_file(
    glob.glob("data/raw/administrative/os_bdline/*/*.gpkg")[0],
    layer="country_region",
    bbox=area
)
data.to_file(gpkgPath, layer="os_bdline_scotland", driver="GPKG")
print("Layer 'os_bdline_scotland' saved!")

# land and water boundary area
data = gpd.overlay(area, bound, how="difference")
data.to_file(gpkgPath, layer="study_area_water", driver="GPKG")
print("Layer 'study_area_water' saved!")

# bounding box around study area
bbox = gpd.GeoDataFrame(geometry=area.buffer(15000).envelope)
bbox.to_file(gpkgPath, layer="study_area_bbox", driver="GPKG")
print("Layer 'study_area_bbox' saved!")

# bounding box around study area intersecting boundary line
data = gpd.overlay(bound, bbox)
data.to_file(gpkgPath, layer="study_area_bdline", driver="GPKG")
print("Layer 'study_area_bdline' saved!")

# ###########################################################
# Community council boundaries
ccb = gpd.read_file(
    glob.glob("data/raw/administrative/ccb/*.shp")[0], mask=area
)

list(ccb)
# ['la_s_code', 'local_auth', 'cc_name', 'active', 'url', 'sh_date_up',
# 'sh_src', 'sh_src_id', 'geometry']

ccb.to_file(gpkgPath, layer="community_council", driver="GPKG")
print("Layer 'community_council' saved!")

# ###########################################################
# OS Terrain 50
layers = fiona.listlayers(
    glob.glob("data/raw/elevation/os_terrain50/*/*.gpkg")[0]
)
for layer in layers:
    data = gpd.read_file(
        glob.glob("data/raw/elevation/os_terrain50/*/*.gpkg")[0],
        layer=layer,
        mask=area
    )
    data.to_file(
        gpkgPath, layer="os_terrain50_"+layer.lower(), driver="GPKG"
    )
    print("Layer 'os_terrain50_" + layer.lower() + "' saved!")

# separate land-water boundary categories
data = gpd.read_file(gpkgPath, layer="os_terrain50_landwaterboundary")

list(data["waterLevelCategory"].unique())
# ['meanHighWater', 'meanLowWater']

data_low = data[data["waterLevelCategory"].isin(["meanLowWater"])]
data_high = data[data["waterLevelCategory"].isin(["meanHighWater"])]

data_low.to_file(gpkgPath, layer="os_terrain50_lowwater", driver="GPKG")

data_high.to_file(gpkgPath, layer="os_terrain50_highwater", driver="GPKG")

# ###########################################################
# Historic Environment Scotland
data = gpd.read_file(glob.glob("data/raw/cultural/sam/*.shp")[0], mask=area)

# assign community council
data = gpd.sjoin(data, ccb[["cc_name", "geometry"]], how="left")
data = data.drop(columns=["index_right"])

# find entries without a community council
list(data["cc_name"].unique())
# ['Airidhantuim', 'Uig', 'Bernera', 'Breasclete', 'Carloway', 'Shawbost',
# 'Ness', nan]
data["cc_name"].fillna("None", inplace=True)
for idx in range(len(data)):
    if data.at[idx, "cc_name"] == "None":
        print(idx, data.at[idx, "DES_TITLE"])
# 24 Beinn an Teampuill, chapel & graveyard, Little Bernera
# 40 St Peter's Church, Pabay Mor, Lewis

# assign community council
# https://canmore.org.uk/site/308737
data.at[24, "cc_name"] = "Bernera"
# https://canmore.org.uk/site/280475
data.at[40, "cc_name"] = "Uig"

data.to_file(gpkgPath, layer="hes_scheduled_monuments", driver="GPKG")
print("Layer 'hes_scheduled_monuments' saved!")

# filter viewpoints
viewpoints = [5390, 5454, 90284, 5548, 90054, 90022, 90110]
viewpoints = ["SM" + str(x) for x in viewpoints]

data = data[data["DES_REF"].isin(viewpoints)]
data["names"] = (data["DES_TITLE"].str.split(",", expand=True)[0])

data.loc[
    data["names"] == "Calanais or Callanish Standing Stones", "names"
] = "Callanish Standing Stones"
data.loc[data["names"] == "Arnol", "names"] = "Arnol Blackhouses"

data.to_file(gpkgPath, layer="viewpoints", driver="GPKG")
print("Layer 'viewpoints' saved!")

# ###########################################################
# NatureScot - GeMS PMF
fiona.listlayers(glob.glob("data/raw/natural/gems_pmf/*.gdb")[0])
# ['GEMS_LSF_POLYGON_DATASET', 'GEMS_SPECIES_LINE_DATASET',
# 'GEMS_HABITAT_POINT_DATASET', 'GEMS_HABITAT_POLYGON_DATASET',
# 'GEMS_SPECIES_POINT_DATASET', 'GEMS_SPECIES_POLYGON_DATASET']

# GEMS_SPECIES_POINT_DATASET
data = gpd.read_file(
    glob.glob("data/raw/natural/gems_pmf/*.gdb")[0],
    layer="GEMS_SPECIES_POINT_DATASET"
)

if data.crs != 27700:
    data = data.to_crs("epsg:27700")
    print("Data reprojected to EPSG:27700")

data = gpd.overlay(data, area)

# drop blank columns
colList = []
for col in list(data):
    if len(data[col].unique()) == 1:
        if list(data[col].unique())[0] is None:
            colList.append(col)

colList.append("name")
colList.append("description")
data.drop(columns=colList, inplace=True)

# map common name to data
species_names = {
    "Cepphus grylle": "Black guillemot",
    "Ammodytes marinus": "Sandeel",
    "Cetorhinus maximus": "Basking shark",
    "Trisopterus esmarkii": "Norway pout",
    "Lutra lutra": "Otter",
    "Dipturus flossada or Dipturus intermedia": "Skate",
    "Halichoerus gryphus": "Grey seal",
    "Phoca vitulina": "Harbour seal",
    "Halichoerus grypus": "Grey seal",
    "Ammodytes": "Sandeel",
    "Anguilla anguilla": "Eel",
    "Pollachius virens": "Saithe",
    "Palinurus elephas": "European spiny lobster",
    "Gadus morhua": "Cod",
    "Arctica islandica": "Ocean quahog",
    "Scomber scombrus": "Atlantic mackerel",
    "Ammodytes tobianus": "Sandeel",
    "Pomatoschistus minutus": "Sand goby",
    "Molva molva": "Ling",
    "Lophius piscatorius": "Anglerfish",
    "Merlangius merlangus": "Whiting"
}

data["common_name"] = data["SCIENTIFIC_NAME"].map(species_names)

data.to_file(gpkgPath, layer="gems_species", driver="GPKG")
print("Layer 'gems_species' saved!")

# ###########################################################
# OS Open Names
layers = glob.glob("data/raw/administrative/os_opennames/*/NB*.csv")
data = pd.read_csv(
    "data/raw/administrative/os_opennames/Docs/OS_Open_Names_Header.csv"
)
list(data)
# ['ID', 'NAMES_URI', 'NAME1', 'NAME1_LANG', 'NAME2', 'NAME2_LANG', 'TYPE',
# 'LOCAL_TYPE', 'GEOMETRY_X', 'GEOMETRY_Y', 'MOST_DETAIL_VIEW_RES',
# 'LEAST_DETAIL_VIEW_RES', 'MBR_XMIN', 'MBR_YMIN', 'MBR_XMAX', 'MBR_YMAX',
# 'POSTCODE_DISTRICT', 'POSTCODE_DISTRICT_URI', 'POPULATED_PLACE',
# 'POPULATED_PLACE_URI', 'POPULATED_PLACE_TYPE', 'DISTRICT_BOROUGH',
# 'DISTRICT_BOROUGH_URI', 'DISTRICT_BOROUGH_TYPE', 'COUNTY_UNITARY',
# 'COUNTY_UNITARY_URI', 'COUNTY_UNITARY_TYPE', 'REGION', 'REGION_URI',
# 'COUNTRY', 'COUNTRY_URI', 'RELATED_SPATIAL_OBJECT', 'SAME_AS_DBPEDIA',
# 'SAME_AS_GEONAMES']

for layer in layers:
    df = pd.read_csv(layer, names=list(data))
    data = pd.concat([data, df])

# well known text with point data
data["wkt"] = (
    "POINT (" + data["GEOMETRY_X"].astype(str) + " " +
    data["GEOMETRY_Y"].astype(str) + ")"
)

data = gpd.GeoDataFrame(
    data, geometry=gpd.GeoSeries.from_wkt(data["wkt"]), crs="EPSG:27700"
)

data = gpd.overlay(data, area)
data = data.drop(columns=[
    "GEOMETRY_X", "GEOMETRY_Y", "wkt", "name", "description"
])

data.to_file(gpkgPath, layer="os_opennames", driver="GPKG")
print("Layer 'os_opennames' saved!")

# ###########################################################
# National Scenic Areas
data = gpd.read_file(glob.glob("data/raw/natural/nsa/*.shp")[0], mask=area)
data.to_file(gpkgPath, layer="national_scenic_areas", driver="GPKG")
print("Layer 'national_scenic_areas' saved!")

# ###########################################################
# Census 2011
data = gpd.read_file(
    glob.glob("data/raw/administrative/census_centroids/*.shp")[0], mask=area
)

list(data)
# ['OBJECTID', 'code', 'masterpc', 'easting', 'northing', 'geometry']

# QS102SC - Population density
data_pop = pd.read_csv("data/raw/administrative/census_data/QS102SC.csv")

list(data_pop)
# ['Unnamed: 0', 'All people', 'Area (hectares)',
# 'Density (number of persons per hectare)']

data_pop.rename(columns={"Unnamed: 0": "code"}, inplace=True)

num_cols = [
    "All people", "Area (hectares)", "Density (number of persons per hectare)"
]

# assign numeric columns
for num in num_cols:
    data_pop[num] = data_pop[num].str.replace(",", "")

data_pop[num_cols] = data_pop[num_cols].apply(pd.to_numeric)

# merge centroids with census data
data_merged = pd.merge(data, data_pop)
data_merged.to_file(gpkgPath, layer="census_centroids", driver="GPKG")
print("Layer 'census_centroids' saved!")

# save census boundaries
data = gpd.read_file(
    glob.glob("data/raw/administrative/census_areas/*.shp")[0], mask=area
)

data.to_file(gpkgPath, layer="census_areas", driver="GPKG")
print("Layer 'census_areas' saved!")

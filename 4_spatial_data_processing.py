import pandas as pd

# If on Windows, geopandas dependencies are a bit tricky. Refer to https://stackoverflow.com/questions/56958421/pip-install-geopandas-on-windows
# geopandas dependencies: pandas (requires GDAL), fiona, pyproj, shapely
# pip install geopandas

import geopandas as gpd
from matplotlib import pyplot as plt

# Close any previously opened plots
plt.close('all')

# Retrieve geodata of the 2020 Neighborhood Tabulation Areas (NTAs) and convert to json
# Retrieve geodata of the 2020 Neighborhood Tabulation Areas (NTAs)
url = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Neighborhood_Tabulation_Areas_2020/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
geodata = gpd.read_file(url)

# Read the raw.csv file 
raw = pd.read_csv('./data/raw.csv')

# Selecting all rows with a specific complaint_type
raw = raw.loc[raw['complaint_type'] == 'UNSANITARY CONDITION']
raw.reset_index(drop=True)

# Converting raw into a geoDataFrame 
# Creating geometry column comprised of longitude and latitude
# Setting crs to match geodata's crs
gpd_raw = gpd.GeoDataFrame(raw, geometry=gpd.points_from_xy(raw['longitude'], raw['latitude'], crs=geodata.crs))

# gpd_raw.plot()
# plt.show(block=False)

# select/confirm that all the points in gpd_raw's geometry are within the geodata's geometry and merge
merge = gpd.sjoin(gpd_raw, geodata, how="inner", op="within")

# merge.plot()
# plt.show(block=False)
import pandas as pd

# If on Windows, geopandas dependencies are a bit tricky. Refer to https://stackoverflow.com/questions/56958421/pip-install-geopandas-on-windows
# geopandas dependencies: pandas (requires GDAL), fiona, pyproj, shapely
# pip install geopandas

import geopandas as gpd
from matplotlib import pyplot as plt

# Close any previously opened plots
plt.close('all')

# Retrieve geodata of the 2020 Neighborhood Tabulation Areas (NTAs) and convert to json
url = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Neighborhood_Tabulation_Areas_2020/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
geodata = gpd.read_file(url)

# Read the raw.csv file 
raw = pd.read_csv('./data/raw.csv')






plt.show(block=False)
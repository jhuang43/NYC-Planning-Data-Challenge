import pandas as pd

# If on Windows, geopandas dependencies are a bit tricky. Refer to https://stackoverflow.com/questions/56958421/pip-install-geopandas-on-windows
# geopandas dependencies: pandas (requires GDAL), fiona, pyproj, shapely
# pip install geopandas

import geopandas as gpd
from matplotlib import pyplot as plt

# Close any previously opened plots
plt.close('all')

# Retrieve geodata of the 2020 Neighborhood Tabulation Areas (NTAs)
url = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Neighborhood_Tabulation_Areas_2020/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
geodata = gpd.read_file(url)

# Read the raw.csv file 
raw = pd.read_csv('./data/raw.csv')

complaint = 'UNSANITARY CONDITION'

# Selecting all rows with a specific complaint_type
raw = raw.loc[raw['complaint_type'] == complaint]
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

# Creating a dataframe that holds the NTA2020 area and count number
NTA_countdf = (merge.groupby("NTA2020").size()).reset_index()
NTA_countdf.columns = ['NTA2020', 'NTA_counts']

# Merging count to geodata and filling NaN count values as 0
choropleth_df = geodata.merge(NTA_countdf, on="NTA2020", how="outer")
choropleth_df['NTA_counts'] = choropleth_df['NTA_counts'].fillna(0)

# Setting size, title, and axis of map
fig, ax = plt.subplots(1, figsize=(11,8.5))
ax.set_title(f"# OF {complaint} COMPLAINTS OVER 7 DAYS")
ax.axis('off')

# Setting colorbar of map
countmin, countmax = 0, choropleth_df['NTA_counts'].max()
choropleth_color = plt.cm.ScalarMappable(cmap="Blues", norm = plt.Normalize(vmin = countmin, vmax = countmax))
choropleth_color.set_array([])
fig.colorbar(choropleth_color)

# Creating choropleth based on NTA_counts, 
choropleth_df.plot(column = 'NTA_counts', cmap = 'Blues', linewidth= 1.0, ax = ax)
plt.show(block = False)
plt.savefig(f'./data/choropleth of {complaint}.png')
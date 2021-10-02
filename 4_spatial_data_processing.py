# On Windows, geopandas dependencies are a bit tricky. Refer to https://stackoverflow.com/questions/56958421/pip-install-geopandas-on-windows
# geopandas dependencies: pandas (requires GDAL), fiona, pyproj, shapely
# pip install geopandas

import geopandas as gpd
from matplotlib import pyplot as plt
import pandas as pd
import os

def create_choropleth(raw_csv, specific_complaint='UNSANITARY CONDITION'):
    """Creates Choropleth map from geodata and csv file.

    If the argument `specific_complaint` isn't passed in, the complaint that will be passed will be 'UNSANITARY CONDITION'.
    
    Parameters
    ----------
    raw_csv : csv
    The csv file that will be passed to create choropleth

    specific_complaint : str, optional
    The complaint_type that the choropleth will be based upon
    """

    # Close any previously opened plots
    plt.close('all')

    # Retrieve geodata of the 2020 Neighborhood Tabulation Areas (NTAs)
    url = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Neighborhood_Tabulation_Areas_2020/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    geodata_gdf = gpd.read_file(url)

    # Selecting all rows with a specific complaint_type
    raw_csv = raw_csv.loc[raw_csv['complaint_type'] == specific_complaint]
    raw_csv.reset_index(drop=True)

    # Converting raw into a geoDataFrame 
    # Creating geometry column comprised of longitude and latitude
    # Setting crs to match geodata's crs
    gpd_raw = gpd.GeoDataFrame(raw_csv, geometry=gpd.points_from_xy(raw_csv['longitude'], raw_csv['latitude'], crs=geodata_gdf.crs))

    # select/confirm that all the points in gpd_raw's geometry are within the geodata's geometry and merge
    merge = gpd.sjoin(gpd_raw, geodata_gdf, how="inner", op="within")

    # Creating a dataframe that holds the NTA2020 area and count number
    NTA_countdf = (merge.groupby("NTA2020").size()).reset_index()
    NTA_countdf.columns = ['NTA2020', 'NTA_counts']

    # Merging count to geodata and filling NaN count values as 0
    choropleth_df = geodata_gdf.merge(NTA_countdf, on="NTA2020", how="outer")
    choropleth_df['NTA_counts'] = choropleth_df['NTA_counts'].fillna(0)

    # Setting size, title, and axis of map
    fig, ax = plt.subplots(1, figsize=(11,8.5))
    ax.set_title(f"# OF {specific_complaint} COMPLAINTS OVER 7 DAYS")
    ax.axis('off')

    # Setting colorbar of map
    countmin, countmax = 0, choropleth_df['NTA_counts'].max()
    choropleth_color = plt.cm.ScalarMappable(cmap="Blues", norm = plt.Normalize(vmin = countmin, vmax = countmax))
    choropleth_color.set_array([])
    fig.colorbar(choropleth_color)

    # Creating choropleth based on NTA_counts, 
    choropleth_df.plot(column = 'NTA_counts', cmap = 'Blues', linewidth= 1.0, ax = ax)
    plt.show(block = False)

def save_plt_as_png(name='file'):
    """Saves plot as a png file.

    If the argument `name` isn't passed in, the file's name will be 'file.png'.
    
    Parameters
    ----------
    name : str, optional
    The name the csv will be saved as
    """

    # Check to see if a data folder exists, if not, make a folder named "data"
    if not os.path.exists('./data'): 
        os.mkdir('./data')

    # Convert and download as png to the data folder    
    plt.savefig(f'./data/{name}.png')


# Read the raw.csv file 
raw = pd.read_csv('./data/raw.csv')

create_choropleth(raw, 'PLUMBING')
save_plt_as_png('choropleth')
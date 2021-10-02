# NYC-Planning-Data-Challenge
Data Challenge for the NYC Planning Data Engineer Position designed to out my skills in python, sql, git, and geospatial data processing.

Code should be run in order of the tasklist, as later tasks rely on previous outputs.
## Dependencies
- Windows 10 (Operating System)
- [Visual Studio Code (IDE)](https://code.visualstudio.com/)
- [Python 3.9.7 (programming language)](https://www.python.org/downloads/)
- [pip (package-management)](https://docs.python.org/3/installing/index.html)
- [PostgreSQL (relational database management system)](https://www.postgresql.org/)

Used libraries:
- **pandas**
- **sodapy**
- **datetime**
- **os**
- **matplotlib**
- **seaborn**
- **geopandas**
  - Installing Fiona(req. for geopandas) and GDAL(req. for Fiona) on Windows through `pip install` has some difficulties. Refer to this [Stack Overflow post](https://stackoverflow.com/questions/56958421/pip-install-geopandas-on-windows) on how to download the `.whl` files for Fiona and GDAL.
- **sqlalchemy**

## Task 1 - 1_data_download.py
This task used Socrata Open Data API to access data in the [311 Service Requests from 2010 to Present](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9). The task was to get records that created **a week ago** and has **HPD** as the responding agency and save those records into a `.csv` file within a `data` folder.
- Used **datetime** and **timedelta** to get the date and time from exactly a week ago
- Queried using the `where` parameter in Socrata client.get to filter created_date and agency
- Saved as `raw.csv` file into `data` folder
## Task 2 - 2_data_aggregation.py
This task used the previously saved `raw.csv` to create a timeseries csv file.
- Created `created_date_hour` column by changing the string back to datetime and inserting just the date and hour
- Created `agency` column by transfering over the column from `raw.csv`
- Created `count` column by grouping the previously created `created_date_hour` column and `agency` column and getting the counts
- Dropped duplicates records
- Saved as `timeseries.csv` file into `data` folder
## Task 3 - 3_data_visualization.py
This task was to create a timeseries multi-line plot and save as a `.png` file. When multi-line plot was initially created, values would not drop to 0 (indicating there were no complaints), so the Cartesian product of all the `created_date_hour` and `complaint_types` was made to fill in those records.
- Created Cartesian product of all `created_date_hour` and all `complaint_types`
- Merged the `timeseries.csv` and Cartesian product
- Replaced NaN values with 0's
- Plotted the multi-line plot
- Saved as `timeseries.png` into `data` folder
## Task 4 - 4_spatial_data_processing.py
This task was to join the [2020 NTA (Neighborhood Tabulation Area) boundaries data](https://www1.nyc.gov/site/planning/data-maps/open-data/census-download-metadata.page) with `raw.csv` to create a choropleth map of a specific complaint's count for the last 7 days
- Retrieved GeoJSON data from site through **geopandas**
- Filtered for a specific `complaint_type` and created a `geometry` column for the `raw.csv` with the `longitude` and `latitude` columns
- Did a spatial join to confirm all points were within the GeoJSON dataFrame
- Created a new DataFrame consisting of to get counts of the NTA areas and merged it with the GeoJSON dataFrame
- Created choropleth map based on the NTA area counts and a colorbar to match
- Saved as `choropleth.png` into `data` folder
## Task 5 - 5_SQL.py
This task was to load `raw.csv` and the csv created in Task 2 (`timeseries.csv`)into a database (PostgreSQL in this case).
- Connected to the PostgreSQL database
- Changed datetime columns of the `.csv` files into timestamps datatypes
- Created/replaced tables in the database
## Task 6
Was unable to complete this task within the time constraints.

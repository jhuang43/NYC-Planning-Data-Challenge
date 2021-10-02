# make sure to install these packages before running:
# pip install pandas

import pandas as pd
import os

def save_as_csv(file_df, name='file'):
    """Saves DataFrame as a csv file.

    If the argument `name` isn't passed in, the file's name will be 'file.csv'.

    Parameters
    ----------
    file_df : DataFrame
    The DataFrame that will be converted to csv

    name : str, optional
    The name the csv will be saved as
    """

    # Check to see if a data folder exists, if not, make a folder named "data"
    if not os.path.exists('./data'): 
        os.mkdir('./data')

    # Convert and download as csv to the data folder without the index    
    file_df.to_csv(f'./data/{name}.csv', index=False)



# Read the csv file
results = pd.read_csv('./data/raw.csv')

# Create an empty DataFrame for the new timeseries
timeseries = pd.DataFrame()

# Convert date to string, with just the date and hour and input into new dataframe
timeseries['created_date_hour'] = pd.to_datetime(results['created_date']).dt.strftime("%Y-%m-%d %H:00")

# Transfer over the complaint types
timeseries['complaint_type'] = results['complaint_type']

# Group over created_date_hour and complaint_type and count and insert as a new column
timeseries['count'] = timeseries.groupby(by=['created_date_hour', 'complaint_type'])['complaint_type'].transform('count')

# Drop duplicates
timeseries = pd.DataFrame.drop_duplicates(timeseries)

# # Checking that the count matches with the original number of records
# results['unique_key'].count()
# timeseries['count'].sum()

# Convert and download as "timeseries.csv" to the data folder without the index
save_as_csv(timeseries, 'timeseries')
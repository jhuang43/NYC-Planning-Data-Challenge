#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
from datetime import datetime, timedelta
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



# Unauthenticated client only works with public data sets. Note 'None' in place of application token, and no username or password:
client = Socrata("data.cityofnewyork.us", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cityofnewyork.us,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# Getting the date from a weekago
date_weekago = (datetime.now() - timedelta(7)).strftime(format = '%Y-%m-%d')

# Results returned as JSON from API / converted to Python list of dictionaries by sodapy.
# Filtered results to select records starting from a week ago and with the agency HPD
results = client.get("erm2-nwe9", where = f"created_date >= '{date_weekago}' and agency = 'HPD'", limit=50000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

# # Check data
# results_df.tail()
# results_df['created_date'].min()
# results_df['created_date'].max()
# results_df['agency'].value_counts()

save_as_csv(results_df, 'raw')
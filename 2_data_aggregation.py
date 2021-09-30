import pandas as pd

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
timeseries.to_csv('./data/timeseries.csv', index = False)
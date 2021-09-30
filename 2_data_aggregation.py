import pandas as pd
results = pd.read_csv('./data/raw.csv')

# Create an empty DataFrame for the new timeseries
timeseries = pd.DataFrame()

# Convert date to string, with just the date and hour and input into new dataframe
timeseries['created_date_hour'] = pd.to_datetime(results['created_date']).dt.strftime("%Y-%m-%d %H:00")

# Transfer over the complaint types
timeseries['complaint_type'] = results['complaint_type']
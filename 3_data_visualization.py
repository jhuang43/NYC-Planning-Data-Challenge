# make sure to install these packages before running:
# pip install pandas
# pip install matplotlib
# pip install seaborn

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# Read the csv file
results = pd.read_csv('./data/timeseries.csv')

# Close any previously opened plots
plt.close('all')

## Create cartesian product dataframe to fill in the days where some complaint counts are 0
# Create lists of unique dates and unique complaints
uniq_date = results['created_date_hour'].unique()
uniq_complaints = results['complaint_type'].unique()

# Create list of complaints for cartesian product
fillcomplaints = []
for i in range(0,len(uniq_date)):
    for x in uniq_complaints:
        fillcomplaints.append(x)

# Create list of dates for cartesian product
filldates = []
for y in uniq_date:
    for i in range(0,len(uniq_complaints)):
        filldates.append(y)

# Created cartesian product dataframe
fill_empty = pd.DataFrame()
fill_empty['created_date_hour'] = filldates
fill_empty['complaint_type'] = fillcomplaints

# Merged Cartesian product dataframe with results and filled in the missing counts with 0's
results = fill_empty.merge(results, how='left', on=['created_date_hour', 'complaint_type'])
results['count'] = results['count'].fillna(0)

# Convert the stringdates to date values and count back to numbers
results['created_date_hour'] = pd.to_datetime(results['created_date_hour'])
results['count'] = pd.to_numeric(results['count'])

# Adjust plot size and axis labels
plt.figure(figsize=(11,8.5), dpi=150, tight_layout = True)
plt.xlabel('Created Date')
plt.ylabel('Count of Complaints')

# Create a multi-line plot based on the count of each complaint over date/time
sns.lineplot(data = results, hue = 'complaint_type', x = 'created_date_hour', y = 'count')

# Show plot
plt.show(block=False)

# Download plot as png image and save to data folder
plt.savefig('./data/timeseries.png')
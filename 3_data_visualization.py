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

# Convert the stringdates to date values and count back to numbers
results['created_date_hour'] = pd.to_datetime(results['created_date_hour'])
results['count'] = pd.to_numeric(results['count'])

# Adjust plot size and axis labels
plt.figure(figsize=(11.5,8), dpi=150, tight_layout = True)
plt.xlabel('Date & Time')
plt.ylabel('Count of Complaints')

# Create a multi-line plot based on the count of each complaint over date/time
sns.lineplot(data = results, hue = 'complaint_type', x = 'created_date_hour', y = 'count')

# Show plot
plt.show(block=False)
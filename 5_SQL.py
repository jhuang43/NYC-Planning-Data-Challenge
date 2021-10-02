# make sure to install these packages before running:
# pip install pandas
# pip install sqlalchemy

import pandas as pd
from sqlalchemy import create_engine

def create_table(engine, csv_filename, tablename):
    """
    Create table from csv file to input into database.

    Parameters
    ----------
    engine : SQLAlchemy engine
    Provides connection to database

    csv_filename: str
    The name of the csv file in the data folder

    tablename: str
    The future name of the table and added to the database
    """
    # Read csv file and changes all column names to be lowercase
    csv_df = pd.read_csv(f'./data/{csv_filename}.csv')
    csv_df.columns = [c.lower() for c in csv_df.columns]

    # Change date types to datetime
    todateformat = []
    for c in csv_df.columns:
        if "date" in c:
            csv_df[c] = csv_df[c].astype('datetime64[ns]')

    # Create/replace table with tablename in db
    csv_df.to_sql (tablename, engine, if_exists='replace', index=False)


# Postgres info
username = 'postgres'
password = 'password'
localhost = '5432'
dbname = 'NYCPlanning'
    
# Connect to the database 
engine = create_engine(f'postgresql://{username}:{password}@localhost:{localhost}/{dbname}')

create_table(engine, 'raw', 'sample_311')
create_table(engine, 'timeseries', 'timeseries')

# Dispose engine
engine.dispose()
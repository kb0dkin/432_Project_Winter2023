import os 
import sqlalchemy
import pandas as pd
from shapely.geometry import Point, Polygon
import time
import psycopg2
import pandas as pd
import geojson
import json
import geopandas as gpd
import requests
user = 'postgres'
password = '432'
ip = '34.134.248.227'
db_name = 'bronze'
port = '5432'


# connect to database


count = 0
for x in range(100, 1000, 100):
    conn = psycopg2.connect(f'host={ip} dbname={db_name} user={user} password={password} port={port}')
    endpoint = f'https://data.cityofchicago.org/resource/m6dm-c72p.json?$query=SELECT%0A%20%20%60trip_id%60%2C%0A%20%20%60trip_start_timestamp%60%2C%0A%20%20%60trip_end_timestamp%60%2C%0A%20%20%60trip_seconds%60%2C%0A%20%20%60trip_miles%60%2C%0A%20%20%60pickup_census_tract%60%2C%0A%20%20%60dropoff_census_tract%60%2C%0A%20%20%60pickup_community_area%60%2C%0A%20%20%60dropoff_community_area%60%2C%0A%20%20%60fare%60%2C%0A%20%20%60tip%60%2C%0A%20%20%60additional_charges%60%2C%0A%20%20%60trip_total%60%2C%0A%20%20%60shared_trip_authorized%60%2C%0A%20%20%60trips_pooled%60%2C%0A%20%20%60pickup_centroid_latitude%60%2C%0A%20%20%60pickup_centroid_longitude%60%2C%0A%20%20%60pickup_centroid_location%60%2C%0A%20%20%60dropoff_centroid_latitude%60%2C%0A%20%20%60dropoff_centroid_longitude%60%2C%0A%20%20%60dropoff_centroid_location%60%0AWHERE%20%60trip_seconds%60%20%3C%20{x}'

    # Pull data from the endpoint with a limit of 1000 rows

    response = requests.get(endpoint).json()

    #convert json to dataframe

    df = pd.DataFrame(response)

    # Recreate the table in the database



    sql_table = 'tnp_trips'


    # Create a cursor object
    cur = conn.cursor()

    # Create the table if it doesn't exist
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {sql_table} (
                    trip_id VARCHAR(100),
                    trip_seconds INT,
                    trip_start_timestamp TIMESTAMP,
                    trip_miles FLOAT,
                    pickup_community_area INT,
                    dropoff_community_area INT,
                    pickup_centroid_latitude FLOAT,
                    pickup_centroid_longitude FLOAT,
                    dropoff_centroid_latitude FLOAT,
                    dropoff_centroid_longitude FLOAT
                )''')

    # Ensure the datatypes are correct


    # insert the data into the table
    for index, row in df.iterrows():
        # if there is a null value, skip the row
        if row.isnull().values.any():
            continue
        print(f'Inserting row {index} into {sql_table}')
        trip_id = row['trip_id']
        trip_seconds = row['trip_seconds']
        trip_start_timestamp = row['trip_start_timestamp']

        trip_miles = row['trip_miles']

        pickup_community_area = row['pickup_community_area']
        dropoff_community_area = row['dropoff_community_area']
        pickup_centroid_latitude = row['pickup_centroid_latitude']
        pickup_centroid_longitude = row['pickup_centroid_longitude']
        dropoff_centroid_latitude = row['dropoff_centroid_latitude']
        dropoff_centroid_longitude = row['dropoff_centroid_longitude']
        trip_id = str(trip_id)
        trip_seconds = int(trip_seconds)
        trip_start_timestamp = str(trip_start_timestamp)
        trip_miles = float(trip_miles)
        pickup_community_area = int(pickup_community_area)
        dropoff_community_area = int(dropoff_community_area)
        pickup_centroid_latitude = float(pickup_centroid_latitude)
        pickup_centroid_longitude = float(pickup_centroid_longitude)
        dropoff_centroid_latitude = float(dropoff_centroid_latitude)
        dropoff_centroid_longitude = float(dropoff_centroid_longitude)

        # insert the row
        cur.execute(f'''INSERT INTO {sql_table} (trip_id, trip_seconds, trip_start_timestamp, trip_miles, pickup_community_area, dropoff_community_area, pickup_centroid_latitude, pickup_centroid_longitude, dropoff_centroid_latitude, dropoff_centroid_longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (trip_id) DO NOTHING''',
                    (row['trip_id'], row['trip_seconds'], row['trip_start_timestamp'], row['trip_miles'], row['pickup_community_area'], row['dropoff_community_area'], row['pickup_centroid_latitude'], row['pickup_centroid_longitude'], row['dropoff_centroid_latitude'], row['dropoff_centroid_longitude']))

    # Commit the changes
    conn.commit()

    # Close the cursor and the connection
    cur.close()
    conn.close()




# This will connect to a postgres database using the public IP address of the VM
# The bronze tables to create the silver tables

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

user = 'postgres'
password = '432'
ip = '34.134.248.227'
db_name = 'bronze'
port = '5432'



# connect to database
conn = psycopg2.connect(f'host={ip} dbname={db_name} user={user} password={password} port={port}')

# select latitude and longitude from the table and run
sql = "SELECT * FROM taxi_trips;"
df = pd.read_sql(sql, conn)
print(df.head())

# load zips.geojson file with geopandas

zips = gpd.read_file('./src/python/zips.geojson')
print(zips.head())

# Takes the latitude and longitude from df and create a zip code column
# Uses reverse_geocoder to find the zip code for each latitude and longitude using the zips.geojson file

lat = df['dropoff_centroid_latitude']
long = df['dropoff_centroid_longitude']

def get_zip(lat, long):
    '''
    Gets the zip code comparing the latitude and longitude to the zips.geojson file
    
    '''
    point = Point(long, lat)
    for i in range(len(zips)):
        if point.within(zips['geometry'][i]):
            return zips['zip'][i]
        else:
            continue

zip_list = []    


for i in range(len(df)):
    zip_list.append(get_zip(lat[i], long[i]))
    if i % 1000 == 0:
        print(i)
    else:
        continue
    
df['zip'] = zip_list

df.to_csv('./src/python/df.csv', encoding='utf-8', index=False)


'''\c silver;

-- taxi/rideshare enum
CREATE TYPE ride_types AS ENUM ('taxi','rideshare');

-- requirement 1: covid in zip codes vs taxis
CREATE TABLE IF NOT EXISTS taxi_covid(
    ind                         SERIAL PRIMARY KEY, -- primary key
    ride_type                   ride_types, -- taxi or rideshare?
    ride_date                   date, -- date of the rides
    zip_start                   int,  -- pick up zip code
    zip_end                     int,  -- destination zip code
    covid_rate                  float, -- weekly covid rate (that's all we've got...)
    num_rides                   int -- number of rides to that zip
);

-- requirement 2 -- taxis from airports to zip codes vs covid rates
--             I think this is just a subset of above...
-- for midway
CREATE TABLE IF NOT EXISTS midway_taxi_covid(
    ind                     SERIAL PRIMARY KEY, -- primary key
    ride_type               ride_types, -- taxi or rideshare?
    ride_date               date, -- date of the rides
    zip                     int,  -- destination zip code
    covid_rate              float, -- weekly covid rate (that's all we've got...)
    num_rides               int -- number of rides to that zip
);
-- for o'hare
CREATE TABLE IF NOT EXISTS ohare_taxi_covid(
    ind                     SERIAL PRIMARY KEY, -- primary key
    ride_type               ride_types, -- taxi or rideshare?
    ride_date               date, -- date of the rides
    zip                     int,  -- destination zip code
    covid_rate              float, -- weekly covid rate (that's all we've got...)
    num_rides               int -- number of rides to that zip
);

-- requirement 3 -- taxi trip #s vs covid vulnerability index
CREATE TABLE IF NOT EXISTS ccvi_taxi(
    trip_id                 varchar(50) PRIMARY KEY, -- trip number
    taxi_id                 varchar(100), -- taxi number; may be NULL if it's ride share
    ride_type               ride_types, -- taxi or rideshare?
    comm_area_start         varchar(100),
    comm_area_end           varchar(100)
);

-- requirement 5 -- building permits by neighborhood with unemployment, poverty, income info
CREATE TABLE IF NOT EXISTS permit_neighborhood(
    permit_id               int PRIMARY KEY, -- building permit id
    neighborhood            varchar(100), -- neighborhood name
    unemployment            float, -- perc over 16yo
    poverty                 float, -- per households
    income                  float
);

-- req 6 -- building permits by zip code, with health measures
CREATE TABLE IF NOT EXISTS permit_zip(
    permit_id               int PRIMARY KEY, -- building permit id
    zip                     int, -- zip code
    unemployment            float, -- perc over 16yo
    poverty                 float, -- per households
    income                  float
);

-- taxi counts (start with just date)
--         we'll split it by type so that we can compare those. Seems interesting
CREATE TABLE IF NOT EXISTS taxi_count(
    id                      SERIAL PRIMARY KEY, -- primary key
    date                    date, 
    zip                     int,
    taxi_count              int,
    rideshare_count         int
);'''

# This will connect to a postgres database using the public IP address of the VM
# The bronze tables to create the silver tables

import os 
import sqlalchemy
import pandas as pd
import geopy

user = 'postgres'
password = '432'
ip = '34.134.248.227'
db_name = 'bronze'
port = '5432'

import psycopg2
import pandas as pd

# connect to database
conn = psycopg2.connect(f'host={ip} dbname={db_name} user={user} password={password} port={port}')

# select latitude and longitude from the table and run
sql = "SELECT * FROM build_permit;"
df = pd.read_sql(sql, conn)
print(df.head())

# create a new column for the coordinates

def get_zipcode(lat, lon):
    return geopy.geocoders.Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36').reverse((lat, lon)).raw['address']['postcode']

for index, row in df.iterrows():
    zipcode = df.loc[index, 'zip'] = get_zipcode(row['latitude'], row['longitude'])
    
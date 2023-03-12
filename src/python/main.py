#import libraries

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

USER = 'postgres'
PASSWORD = '432'
IP = '34.134.248.227'
DB_NAME = 'bronze'
PORT = '5432'

import pandas as pd

def build_permit():
    
    DATASET = 'ydr8-5enu'
    # Paginate through 100,000 rows 1000 at a time starting at 0
    for page in range(0, 10000, 1000):
        conn = psycopg2.connect(f'host={IP} dbname={DB_NAME} user={USER} password={PASSWORD} port={PORT}')
        endpoint = f'https://data.cityofchicago.org/resource/{DATASET}.json?$order=:id%20DESC&$limit=1000&$offset={page}'
        
        response = requests.get(endpoint).json()
        
        df = pd.DataFrame(response)
        
        SQL_TABLE = 'build_permit'
        
        cur = conn.cursor()
        
        for index, row in df.iterrows():
            
            #skip any rows that are missing data
            if row['id'] == '' or row['permit_'] == '' or row['permit_type'] == '' or row['application_start_date'] == '' or row['issue_date'] == '' or row['community_area'] == '' or row['ward'] == '' or row['latitude'] == '' or row['longitude'] == '':
                continue
            
            try:
                print(f'Inserting row {index} into {SQL_TABLE}')
                
                id = row['id']
                permit_ = row['permit_']
                permit_type = row['permit_type']
                application_start_date = row['application_start_date']
                issue_date = row['issue_date']
                community_area = row['community_area']
                ward = row['ward']
                latitude = row['latitude']
                longitude = row['longitude']
                
                #correct data types
                id = int(id)
                permit_ = int(permit_)
                permit_type = str(permit_type)
                application_start_date = str(application_start_date)
                
                #fix issue date
                application_start_date = application_start_date[0:10]
                
                issue_date = str(issue_date)
                issue_date = issue_date[0:10]
                community_area = int(community_area)
                ward = int(ward)
                latitude = float(latitude)
                longitude = float(longitude)
                
                
                
                #insert data into table
                cur.execute(f"INSERT INTO {SQL_TABLE} (id, permit_, permit_type, application_start_date, issue_date, community_area, ward, latitude, longitude) VALUES ({id}, {permit_}, '{permit_type}', '{application_start_date}', '{issue_date}', {community_area}, {ward}, {latitude}, {longitude}) ON CONFLICT DO NOTHING;")
                
                conn.commit()
            except Exception as e:
                print(e)
                continue
        
def covid_19_daily_cases():

    '''type Trip []struct {
        LabReportDate                        string `json:"lab_report_date"`
        CasesTotal                           string `json:"cases_total"`
        DeathsTotal                          string `json:"deaths_total"`
        HospitalizationsTotal                string `json:"hospitalizations_total"`	
    }'''                
                    
    DATA_SET = 'naz8-j4nc'
    
    for page in range(0, 10000, 1000):
        conn = psycopg2.connect(f'host={IP} dbname={DB_NAME} user={USER} password={PASSWORD} port={PORT}')
        endpoint = f'https://data.cityofchicago.org/resource/{DATA_SET}.json?$order=:id%20DESC&$limit=1000&$offset={page}'
        
        response = requests.get(endpoint).json()
        
        df = pd.DataFrame(response)
        
        SQL_TABLE = 'covid_19_daily_cases'
        
        cur = conn.cursor()
        
        for index, row in df.iterrows():
            
            #skip any rows that are missing data
            if row['lab_report_date'] == '' or row['cases_total'] == '' or row['deaths_total'] == '' or row['hospitalizations_total'] == '':
                continue
            
            try:
                print(f'Inserting row {index} into {SQL_TABLE}')
                
                lab_report_date = row['lab_report_date']
                cases_total = row['cases_total']
                deaths_total = row['deaths_total']
                hospitalizations_total = row['hospitalizations_total']
                
                #correct data types
                lab_report_date = str(lab_report_date)
                lab_report_date = lab_report_date[0:10]
                cases_total = int(cases_total)
                deaths_total = int(deaths_total)
                hospitalizations_total = int(hospitalizations_total)
                
                #insert data into table
                cur.execute(f"INSERT INTO {SQL_TABLE} (lab_report_date, cases_total, deaths_total, hospitalizations_total) VALUES ('{lab_report_date}', {cases_total}, {deaths_total}, {hospitalizations_total}) ON CONFLICT DO NOTHING;")
                
                conn.commit()
            except Exception as e:
                print(e)
                continue

def covid_19_zip():
    '''
    zip_code                                              Unknown
    week_number                                                 9
    week_start                            2023-02-26T00:00:00.000
    week_end                              2023-03-04T00:00:00.000
    cases_weekly                                               16
    cases_cumulative                                         4578
    case_rate_weekly                                            0
    case_rate_cumulative                                        0
    tests_weekly                                              389
    tests_cumulative                                       237058
    test_rate_weekly                                            0
    test_rate_cumulative                                        0
    percent_tested_positive_weekly                          0.044
    percent_tested_positive_cumulative                      0.087
    deaths_weekly                                               0
    deaths_cumulative                                          13
    death_rate_weekly                                           0
    death_rate_cumulative                                       0
    population                                                  0
    row_id                                         Unknown-2023-9
    zip_code_location                                         NaN
    '''
    
    
    DATASET = 'yhhz-zm2v'
    
    for page in range(0, 10000, 1000):
        conn = psycopg2.connect(f'host={IP} dbname={DB_NAME} user={USER} password={PASSWORD} port={PORT}')
        endpoint = f'https://data.cityofchicago.org/resource/{DATASET}.json?$order=:id%20DESC&$limit=1000&$offset={page}'
        
        response = requests.get(endpoint).json()
        
        df = pd.DataFrame(response)
        
        SQL_TABLE = 'covid_19_zip'
        
        cur = conn.cursor()
        
        for index, row in df.iterrows():
            
            #skip any rows that are missing data
            if row['zip_code'] == 'Unknown' or row['week_number'] == '' or row['week_start'] == '' or row['cases_weekly'] == '' or row['case_rate_cumulative'] == '' or row['deaths_weekly'] == '' or row['death_rate_weekly'] == '':
                continue
            
            try:
                print(f'Inserting row {index} into {SQL_TABLE}')
                
                zip_code = row['zip_code']
                if zip_code == 'Unknown':
                    zip_code = 0
                week_number = row['week_number']
                week_start = row['week_start']
                cases_weekly = row['cases_weekly']
                case_rate_cumulative = row['case_rate_cumulative']
                deaths_weekly = row['deaths_weekly']
                death_rate_weekly = row['death_rate_weekly']
                row_id = row['row_id']
                
                #correct data types
                zip_code = int(zip_code)
                week_number = int(week_number)
                week_start = str(week_start)
                week_start = week_start[0:10]
                cases_weekly = int(cases_weekly)
                case_rate_cumulative = float(case_rate_cumulative)
                deaths_weekly = int(deaths_weekly)
                death_rate_weekly = float(death_rate_weekly)
                row_id = str(row_id)
                
                #insert data into table
                cur.execute(f"INSERT INTO {SQL_TABLE} (row_id, zip_code, week_number, week_start, cases_weekly, case_rate_cumulative, deaths_weekly, death_rate_weekly) VALUES ('{row_id}', '{zip_code}', {week_number}, '{week_start}', {cases_weekly}, {case_rate_cumulative}, {deaths_weekly}, {death_rate_weekly}) ON CONFLICT DO NOTHING;")
                
                conn.commit()
            except Exception as e:
                print(e)
                print(row)
                continue
    
    
def health_ind():
    '''
         -- health_ind :    table of health and other community indicators
        CREATE TABLE IF NOT EXISTS health_ind(
        community_area              int PRIMARY KEY, -- this doesn't match the other info!
        community_area_name         varchar(100), -- community area name
        below_poverty_level         float, -- percent of households in below poverty level
        no_high_school_diploma      float, -- percent persons >25yo
        per_capita_income           float, -- dollars
        unemployment                float  -- percent of persons >16yo

    
         
    '''
         
    DATASET = 'iqnk-2tcu'
    
    for page in range(0, 10000, 1000):
        conn = psycopg2.connect(f'host={IP} dbname={DB_NAME} user={USER} password={PASSWORD} port={PORT}')
        endpoint = f'https://data.cityofchicago.org/resource/{DATASET}.json?$order=:id%20DESC&$limit=1000&$offset={page}'
        
        response = requests.get(endpoint).json()
        
        df = pd.DataFrame(response)
        
        SQL_TABLE = 'health_ind'
        
        cur = conn.cursor()
        
        for index, row in df.iterrows():
            
            #skip any rows that are missing data
            if row['community_area'] == '' or row['community_area_name'] == '' or row['below_poverty_level'] == '' or row['no_high_school_diploma'] == '' or row['per_capita_income'] == '' or row['unemployment'] == '':
                continue
            
            try:
                print(f'Inserting row {index} into {SQL_TABLE}')
                
                community_area = row['community_area']
                community_area_name = row['community_area_name']
                below_poverty_level = row['below_poverty_level']
                no_high_school_diploma = row['no_high_school_diploma']
                per_capita_income = row['per_capita_income']
                unemployment = row['unemployment']
                
                #correct data types
                community_area = int(community_area)
                community_area_name = str(community_area_name)
                below_poverty_level = float(below_poverty_level)
                no_high_school_diploma = float(no_high_school_diploma)
                per_capita_income = int(per_capita_income)
                unemployment = float(unemployment)
                
                #insert data into table
                cur.execute(f"INSERT INTO {SQL_TABLE} (community_area, community_area_name, below_poverty_level, no_high_school_diploma, per_capita_income, unemployment) VALUES ({community_area}, '{community_area_name}', {below_poverty_level}, {no_high_school_diploma}, {per_capita_income}, {unemployment}) ON CONFLICT DO NOTHING;")
                
                conn.commit()
            except Exception as e:
                print(e)
                continue

def taxi_trips():
    '''
    CREATE TABLE IF NOT EXISTS taxi_trips(
    trip_id                     varchar(50) PRIMARY KEY, -- trip id hash 
    taxi_id                     varchar(128), -- taxi id hash
    trip_start_timestamp        date, -- start of trip
    trip_seconds                int, -- trip length in seconds
    trip_miles                  float, -- not very useful, since this is really based off census tracts...
    pickup_centroid_latitude    float, -- latitude of pickup location
    pickup_centroid_longitude   float, -- longitude of pickup location
    dropoff_centroid_latitude   float, -- latitude of dropoff location
    dropoff_centroid_longitude  float, -- longitude of dropoff location
    pickup_community_area       int, -- community area number of the pickup location. Blank outside Chicago
    dropoff_community_area      int -- community area number of the dropoff location. Blank outside Chicago
);
    
    '''
    
    DATASET = 'wrvz-psew'
    
    for page in range(0, 10000, 1000):
        conn = psycopg2.connect(f'host={IP} dbname={DB_NAME} user={USER} password={PASSWORD} port={PORT}')
        endpoint = f'https://data.cityofchicago.org/resource/{DATASET}.json?$order=:id%20DESC&$limit=1000&$offset={page}'
        
        response = requests.get(endpoint).json()
        
        df = pd.DataFrame(response)
        
        SQL_TABLE = 'taxi_trips'
        
        cur = conn.cursor()
        
        for index, row in df.iterrows():
            
            #skip any rows that are missing data
            if row['trip_id'] == '' or row['taxi_id'] == '' or row['trip_start_timestamp'] == '' or row['trip_seconds'] == '' or row['trip_miles'] == '' or row['pickup_centroid_latitude'] == '' or row['pickup_centroid_longitude'] == '' or row['dropoff_centroid_latitude'] == '' or row['dropoff_centroid_longitude'] == '' or row['pickup_community_area'] == '' or row['dropoff_community_area'] == '':
                continue
            
            try:
                print(f'Inserting row {index} into {SQL_TABLE}')
                
                trip_id = row['trip_id']
                taxi_id = row['taxi_id']
                trip_start_timestamp = row['trip_start_timestamp']
                trip_seconds = row['trip_seconds']
                trip_miles = row['trip_miles']
                pickup_centroid_latitude = row['pickup_centroid_latitude']
                pickup_centroid_longitude = row['pickup_centroid_longitude']
                dropoff_centroid_latitude = row['dropoff_centroid_latitude']
                dropoff_centroid_longitude = row['dropoff_centroid_longitude']
                pickup_community_area = row['pickup_community_area']
                dropoff_community_area = row['dropoff_community_area']
                
                #correct data types
                trip_id = str(trip_id)
                taxi_id = str(taxi_id)
                trip_start_timestamp = str(trip_start_timestamp)
                trip_seconds = int(trip_seconds)
                trip_miles = float(trip_miles)
                pickup_centroid_latitude = float(pickup_centroid_latitude)
                pickup_centroid_longitude = float(pickup_centroid_longitude)
                dropoff_centroid_latitude = float(dropoff_centroid_latitude)
                dropoff_centroid_longitude
                pickup_community_area = int(pickup_community_area)
                dropoff_community_area = int(dropoff_community_area)
                
                #insert data into table
                cur.execute(f"INSERT INTO {SQL_TABLE} (trip_id, taxi_id, trip_start_timestamp, trip_seconds, trip_miles, pickup_centroid_latitude, pickup_centroid_longitude, dropoff_centroid_latitude, dropoff_centroid_longitude, pickup_community_area, dropoff_community_area) VALUES ('{trip_id}', '{taxi_id}', '{trip_start_timestamp}', {trip_seconds}, {trip_miles}, {pickup_centroid_latitude}, {pickup_centroid_longitude}, {dropoff_centroid_latitude}, {dropoff_centroid_longitude}, {pickup_community_area}, {dropoff_community_area}) ON CONFLICT DO NOTHING;")
                
                conn.commit()
            except Exception as e:
                print(e)
                continue

def tnp_trips():
    
    '''
    type Trip []struct {
	TripID                  string `json:"trip_id"`
	TripSeconds             string `json:"trip_seconds"`
	TripStartTimestamp	  string `json:"trip_start_timestamp"`
	TripMiles               string `json:"trip_miles"`
	PickupCommunityArea     string `json:"pickup_community_area"`
	DropoffCommunityArea    string `json:"dropoff_community_area"`
	PickupCentroidLatitude  string `json:"pickup_centroid_latitude"`
	PickupCentroidLongitude string `json:"pickup_centroid_longitude"`
	DropoffCentroidLatitude  string `json:"dropoff_centroid_latitude"`
	DropoffCentroidLongitude string `json:"dropoff_centroid_longitude"`
}
    CREATE TABLE IF NOT EXISTS tnp_trips(
    trip_id                     VARCHAR(50) PRIMARY KEY, -- trip id hash 
    trip_seconds                int,
    trip_start_timestamp        date,    -- trip length in seconds
    trip_miles                  float,    -- not very useful, since this is really based off census tracts...
    pickup_community_area       int,    -- community area number. blank outside chicago
    dropoff_community_area      int,    -- community area number. blank outside chicago
    pickup_centroid_latitude    float,    -- latitude of pickup location
    pickup_centroid_longitude   float,    -- longitude of pickup location
    dropoff_centroid_latitude   float,    -- latitude of dropoff location
    dropoff_centroid_longitude  float    -- longitude of dropoff location
);
    '''
    
    DATASET = 'm6dm-c72p'
    
    for page in range(0, 10000, 1000):
        conn = psycopg2.connect(f'host={IP} dbname={DB_NAME} user={USER} password={PASSWORD} port={PORT}')
        endpoint = f'https://data.cityofchicago.org/resource/{DATASET}.json?$order=:id%20DESC&$limit=1000&$offset={page}'
        
        response = requests.get(endpoint).json()
        
        df = pd.DataFrame(response)
        
        SQL_TABLE = 'tnp_trips'
        
        cur = conn.cursor()
        
        for index, row in df.iterrows():
            
            #skip any rows that are missing data
            if row['trip_id'] == '' or row['trip_seconds'] == '' or row['trip_start_timestamp'] == '' or row['trip_miles'] == '' or row['pickup_community_area'] == '' or row['dropoff_community_area'] == '' or row['pickup_centroid_latitude'] == '' or row['pickup_centroid_longitude'] == '' or row['dropoff_centroid_latitude'] == '' or row['dropoff_centroid_longitude'] == '':
                continue
            
            try:
                print(f'Inserting row {index} into {SQL_TABLE}')
                
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
                
                #correct data types
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
                
                #insert data into table
                cur.execute(f"INSERT INTO {SQL_TABLE} (trip_id, trip_seconds, trip_start_timestamp, trip_miles, pickup_community_area, dropoff_community_area, pickup_centroid_latitude, pickup_centroid_longitude, dropoff_centroid_latitude, dropoff_centroid_longitude) VALUES ('{trip_id}', {trip_seconds}, '{trip_start_timestamp}', {trip_miles}, {pickup_community_area}, {dropoff_community_area}, {pickup_centroid_latitude}, {pickup_centroid_longitude}, {dropoff_centroid_latitude}, {dropoff_centroid_longitude}) ON CONFLICT DO NOTHING;")
                
                conn.commit()
            except Exception as e:
                print(e)
                continue

def ccvi_index():
       
    
    DATASET = 'xhc6-88s9'
    
    #This data set is only two pages long, so we don't need to loop through pages
    
    conn = psycopg2.connect(f'host={IP} dbname={DB_NAME} user={USER} password={PASSWORD} port={PORT}')
    endpoint = f'https://data.cityofchicago.org/resource/{DATASET}.json'
    
    response = requests.get(endpoint).json()
    
    df = pd.DataFrame(response)
    
    SQL_TABLE = 'ccvi_index'
    print(len(df))
    #data types
    
    # geography_type = str(df['geography_type'])
    # community_area_or_zip = int(df['community_area_or_zip'])
    # ccvi_score = float(df['ccvi_score'])
    # ccvi_category = str(df['ccvi_category'])
    # latitude = float(df['location']['coordinates'][1])
    # longitude = float(df['location']['coordinates'][0])
    # community_area_name = str(df['community_area_name'])
    # create table if there is not one already
    
    #Delete table if it already exists
    cur = conn.cursor()
    cur.execute(f'DROP TABLE IF EXISTS {SQL_TABLE}')
    conn.commit()
    
    create_table = f'''
    CREATE TABLE IF NOT EXISTS {SQL_TABLE}(geography_type VARCHAR(50), community_area_or_zip int, ccvi_score float, ccvi_category VARCHAR(50), latitude float, longitude float, community_area_name VARCHAR(50));
    '''
    
    cur = conn.cursor()
    cur.execute(create_table)
    conn.commit()
    
    for index, row in df.iterrows():
        
                
        try:
            print(f'Inserting row {index} into {SQL_TABLE}')
            
            geography_type = row['geography_type']
            community_area_or_zip = row['community_area_or_zip']
            ccvi_score = row['ccvi_score']
            ccvi_category = row['ccvi_category']
            latitude = row['location']['coordinates'][1]
            longitude = row['location']['coordinates'][0]
            community_area_name = row['community_area_name']
            
            #correct data types
            geography_type = str(geography_type)
            community_area_or_zip = int(community_area_or_zip)
            ccvi_score = float(ccvi_score)
            ccvi_category = str(ccvi_category)
            latitude = float(latitude)
            longitude = float(longitude)
            community_area_name = str(community_area_name)
            if community_area_name == 'nan':
                community_area_name = ''
            
            #insert data into table
            cur.execute(f"INSERT INTO {SQL_TABLE} (geography_type, community_area_or_zip, ccvi_score, ccvi_category, latitude, longitude, community_area_name) VALUES ('{geography_type}', {community_area_or_zip}, {ccvi_score}, '{ccvi_category}', {latitude}, {longitude}, '{community_area_name}') ON CONFLICT DO NOTHING;")
            
            conn.commit()
        except Exception as e:
            print(e)
            continue
    
    
    cur = conn.cursor()
    
    for index, row in df.iterrows():
        
        #skip any rows that are missing data
        if row['trip_id'] == '' or row['taxi_id'] == '' or row['trip_start_timestamp'] == '' or row['trip_end_timestamp'] == '' or row['trip_seconds'] == '' or row['trip_miles'] == '' or row['pickup_census_tract'] == '' or row['dropoff_census_tract'] == '' or row['pickup_community_area'] == '' or row['dropoff_community_area'] == '' or row['fare'] == '' or row['tips'] == '' or row['tolls'] == '' or row['extras'] == '' or row['trip_total'] == '' or row['payment_type'] == '' or row['company'] == '' or row['pickup_latitude'] == '' or row['pickup_longitude'] == '' or row['dropoff_latitude'] == '' or row['dropoff_longitude'] == '':
            continue
        
        try:
            print(f'Inserting row {index} into {SQL_TABLE}')
            
            trip_id = row['trip_id']
            taxi_id = row['taxi_id']
            ride_type = row['ride_type']
        except Exception as e:
            print(e)
            continue
            

def main():
    # build_permit()
    # covid_19_daily_cases()
    # covid_19_zip()
    # health_ind()
    # taxi_trips()
    # tnp_trips()
    ccvi_index()


if __name__ == "__main__":
    main()
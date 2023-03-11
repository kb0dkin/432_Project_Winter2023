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
    for page in range(0, 100000, 1000):
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
        
            
                    
    

def main():
    build_permit()


if __name__ == "__main__":
    main()
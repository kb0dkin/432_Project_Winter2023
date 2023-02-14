import os
import requests
import json
from sodapy import Socrata

API_KEY = os.environ.get('API_KEY')
SECRET_API = os.environ.get('SECRET_API')
APP_TOKEN = os.environ.get('APP_TOKEN')
SECRET_APP_TOKEN = os.environ.get('SECRET_APP')


#examples of API calls
#https://data.cityofchicago.org/resource/wrvz-psew.json
#https://data.cityofchicago.org/resource/wrvz-psew.json?trip_start_timestamp=2023-02-01T00:00:00.000
#https://data.cityofchicago.org/resource/u77m-8jgp.json?$where=total_passing_vehicle_volume > 20000

def get_data(dataset, query):
    try:
        '''
        Makes an API call to the Chicago Data Portal and returns the data in JSON format.
        dataset is the dataset ID, and query is the query string.
        '''
        response = requests.get(f'https://data.cityofchicago.org/resource/{dataset}.json?${query}')
        print(response.json())
        with open('datad.json', 'w') as outfile:
            json.dump(response.json(), outfile)
        return response.json()

    except:
        print('Error')
    
get_data('wrvz-psew', 'where=trip_miles > 100')
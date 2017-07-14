#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Este script toma un archivo CSV y lo geolocaliza, es decir crea un nuevo archivo _geo.csv con columnas lat y long.
# Utiliza el API de Google Maps
# Instrucciones en como obtener la API Key para Google Maps: https://github.com/slawek87/geolocation-python

from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient
import os
import argparse
import csv
import sys

# get address to geolocalize
# geolocalize
# save it in file_geo.csv

# environment variables:
#                   GOOGLE_MAPS_API_KEY
#                   COUNTRY

# arguments:
#                   COLUMN NAMES

def get_environment_variables():
    if not os.environ.has_key('COUNTRY') or not os.environ.has_key('GOOGLE_MAPS_API_KEY'):
        sys.exit('Variables de ambiente COUNTRY o GOOGLE_MAPS_API_KEY no estan definidas.')
    # look for environment variables
    return {'country': os.environ['COUNTRY'], 'api_key': os.environ['GOOGLE_MAPS_API_KEY']}

def get_address(row, fields, country):
    address = ', '.join(map(lambda x: row[x], fields.split(','))) + ', ' + country
    return address

def main():

    parser = argparse.ArgumentParser(description='Geolocalizer un archivo CSV.')
    parser.add_argument('--csv', help='nombre del archivo CSV a geolocalizar')
    parser.add_argument('--columnas', help='las columnas (en orden) de la dirección')

    args = parser.parse_args()

    # get file name and column names from arguments
    csv_file = args.csv
    new_csv_file = '_'.join([csv_file.split('.')[0], 'geo.csv'])

    # get the columns names where the address is
    fields = args.columnas

    # get api key and country from environment variables
    env_variables = get_environment_variables()

    # get an instance of google maps
    google_maps = GoogleMaps(api_key=env_variables['api_key'])

    with open(csv_file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        with open(new_csv_file, 'wb') as newcsvfile:
            writer = csv.DictWriter(newcsvfile)
            for row in reader:
                address = get_address(row, fields, env_variables['country'])
                location = google_maps.search(location=address) # sends search to Google Maps.
                my_location = location.first() # returns only first location.

                row['lat'] = my_location.lat
                row['long'] = my_location.lng
                writer.writerow(row)

if __name__ == '__main__':
    main()
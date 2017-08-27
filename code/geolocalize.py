#!/usr/bin/python
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
import logging
import time

## SAVE THE FILE TO A GEOJSON

# the template. where data from the csv will be formatted to geojson
template = \
    ''' \
    { "type" : "Feature",
        "geometry" : {
            "type" : "Point",
            "coordinates" : [%s, %s]},
        "properties" : %s
        },
    '''

## GEOLOCALIZATION

# get address to geolocalize
# geolocalize
# save it in file_geo.csv

# environment variables:
#                   GOOGLE_MAPS_API_KEY
#                   COUNTRY

# arguments:
#                   COLUMN NAMES

def convert_row(row):
    properties = {}
    for i in row:
        if i != 'lng' or i != 'lat':
            properties[i] = row[i]
    return template % (row['lng'], row['lat'],  properties)

def get_environment_variables():
    if not os.environ.has_key('COUNTRY') or not os.environ.has_key('GOOGLE_MAPS_API_KEY'):
        sys.exit('Variables de ambiente COUNTRY o GOOGLE_MAPS_API_KEY no estan definidas.')
    # look for environment variables
    return {'country': os.environ['COUNTRY'], 'api_key': os.environ['GOOGLE_MAPS_API_KEY']}

def get_address(row, fields, country):
    address = ', '.join(map(lambda x: row[x], fields.split(','))) + ', ' + country
    return address

def main():

    logging_file = 'geolocation_%s.log' % time.strftime("%H_%M_%S")
    logging.basicConfig(filename=logging_file,level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Geolocalizer un archivo CSV.')
    parser.add_argument('--csv', help='nombre del archivo CSV a geolocalizar')
    parser.add_argument('--columnas', help='las columnas (en orden) de la dirección')

    args = parser.parse_args()

    # get file name and column names from arguments
    csv_file = args.csv
    new_csv_file = '_'.join([csv_file.split('.')[0], 'geo.csv'])

    new_geojson_file = '_'.join([csv_file.split('.')[0], '.geojson'])

    # get the columns names where the address is
    fields = args.columnas

    # get api key and country from environment variables
    env_variables = get_environment_variables()

    # get an instance of google maps
    google_maps = GoogleMaps(api_key=env_variables['api_key'])

    # the head of the geojson file
    output = \
        ''' \
    { "type" : "Feature Collection",
        "features" : [
        '''
    with open(csv_file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        fieldnames.append('lat')
        fieldnames.append('lng')
        with open(new_csv_file, 'wb') as newcsvfile:
            writer = csv.DictWriter(newcsvfile, fieldnames=fieldnames)
            for row in reader:
                address = get_address(row, fields, env_variables['country'])
                try:
                    location = google_maps.search(location=address) # sends search to Google Maps.
                    my_location = location.first() # returns only first location.

                    if my_location != None:
                        row['lat'] = my_location.lat
                        row['lng'] = my_location.lng
                        writer.writerow(row)
                except:
                    e = sys.exc_info()[0]
                    logging.warning("<p>LOG: no pudo encontrar la dirección: '%s' . Error: %s</p>", address, e)

                output += convert_row(row)

        # convert new file into a geojson file
        # the tail of the geojson file
        output += \
            ''' \
            ]
        }
            '''
        # opens an geoJSON file to write the output to
        outFileHandle = open(new_geojson_file, "w")
        outFileHandle.write(output)
        outFileHandle.close()

if __name__ == '__main__':
    main()

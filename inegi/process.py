#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas
import logging
import time
import argparse
import sys

# CVE_ENT: clave de la entidad
# CVE_MUN: clave del municipio
# CVE_LOC: clave de localidad
# NOM_LOC: nombre de la localidad

# CVE_ENT: clave de la entidad
# NOM_ENT: nombre de la entidad
# CVE_MUN: clave del municipio
# NOM_MUN: nombre del municipio
# CVE_LOC: clave de la localidad
# NOM_LOC: nombre de la localidad

def main():
    print "ACA-1"
    # get inegi data
    inegi_csv = 'ARCH445.CSV'
    inegi = pandas.read_csv(inegi_csv)
    print "ACA0"
    # get file to merge
    # get field for the NOM_LOC

    logging_file = 'inegi_%s.log' % time.strftime("%H_%M_%S")
    logging.basicConfig(filename=logging_file,level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Agregar codigos de INEGI al CSV.')
    parser.add_argument('--csv', help='nombre del archivo CSV a unir')
    parser.add_argument('--estado', help='el campo que tiene el nombre del estado')
    parser.add_argument('--municipio', help='el campo que tiene el nombre del municipio')
    parser.add_argument('--localidad', help='el campo que tiene el nombre de la localidad')

    args = parser.parse_args()

    # get file name and column names from arguments
    csv_file = args.csv
    new_csv_file = '_'.join([csv_file, 'inegi.csv'])

    print "ACA1"
    estado = args.estado
    municipio = args.municipio
    localidad = args.localidad
    print "ACA2"
    data_to_merge = pandas.read_csv(csv_file)

    print "ACA3"
    # Merging data into the inegi data
    try:
        enriched_data = data_to_merge.merge(inegi, how='left', left_on=[estado,municipio,localidad], right_on=['NOM_ENT','NOM_MUN','NOM_LOC'], left_index=False, right_index=False, sort=False, suffixes=('', '_a'), copy=True, indicator=False)
        enriched_data.to_csv(new_csv_file, encoding='utf-8')
    except:
        e = sys.exc_info()[0]
        logging.warning("<p>LOG: error when merging data: %s</p>", e)


if __name__ == '__main__':
    main()

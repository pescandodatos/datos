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

# How to use it: an example
# python process.py --csv ../rnpa/embarcaciones_detalles.csv --estado ESTADO --municipio MUNICIPIO --localidad LOCALIDAD

#,RNPA_ACTIVO,NOMBRE_EMBARCACION,RNPA_UNIDAD_ECONOMICA,NOMBRE_UNIDAD_ECONOMICA,ESTADO,MUNICIPIO,LOCALIDAD,TIPO_EMBARCACION,FECHA_REGISTRO,NOMBRE_EMBARCACION_a,TIPO,MUNICIPIO_a,LOCALIDAD_a,ESTADO_a,ANO_CONSTRUCCION,TIPO_ua,NOMBRE_UNIDAD_ECONOMICA_ua,FECHA_REGISTRO_ua,TIPO_PERSONA,REPRESENTANTE_LEGAL,ESTADO_ua,MUNICIPIO_ua,LOCALIDAD_ua,INICIO

def main():
    # get inegi data
    inegi_csv = 'inegi.csv'
    inegi = pandas.read_csv(inegi_csv, encoding='utf-8')

    # get file to merge
    # get field for the NOM_LOC

    logging_file = 'inegi_%s.log' % time.strftime("%H_%M_%S")
    logging.basicConfig(filename=logging_file,level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Agregar codigos de INEGI al CSV.')
    parser.add_argument('--csv', help='nombre del archivo CSV a unir')
    parser.add_argument('--estado', help='el campo que tiene el nombre del estado')
    parser.add_argument('--municipio', help='el campo que tiene el nombre del municipio')
    parser.add_argument('--localidad', help='el campo que tiene el nombre de la localidad')
    parser.add_argument('--inegi', help='el nuevo campo donde agregar el codigo de inegi')
    

    args = parser.parse_args()

    # get file name and column names from arguments
    csv_file = args.csv

    if csv_file == None:
        sys.exit("Necesitamos un archivo CSV.")

    new_csv_file = '_'.join([csv_file, 'inegi.csv'])

    estado = args.estado
    municipio = args.municipio
    localidad = args.localidad

    new_column = args.inegi

    # rename columns
    inegi[estado] = inegi['NOM_ENT']
    inegi[municipio] = inegi['NOM_MUN']
    inegi[localidad] = inegi['NOM_LOC']

    # UpperCase to everything & select only columns that we need
    clean_inegi = inegi[[estado, municipio, localidad, 'CVE_ENT', 'CVE_MUN', 'CVE_LOC']]
    clean_inegi = clean_inegi.apply(lambda x: x.astype('unicode').str.upper())

    inegi.set_index([estado, municipio, localidad])

    data_to_merge = pandas.read_csv(csv_file)
    data_to_merge.apply(lambda x: x.astype('str').str.upper())
    data_to_merge.set_index([estado, municipio, localidad])

    # Merging data into the inegi data
    try:
        enriched_data = data_to_merge.merge(clean_inegi, how='left')
        
        enriched_data[new_column] = enriched_data.CVE_ENT.str.cat(enriched_data.CVE_MUN.str.cat(enriched_data.CVE_LOC))

        enriched_data.drop('CVE_ENT',1, inplace=True)  
        enriched_data.drop('CVE_MUN',1, inplace=True)
        enriched_data.drop('CVE_LOC',1, inplace=True)

        enriched_data.to_csv(new_csv_file, sep=',', encoding='utf-8')


    except:
        e = sys.exc_info()[0]
        logging.warning("<p>LOG: error when merging data: %s</p>", e)


if __name__ == '__main__':
    main()


#cell.cross("inegi", "ESTADO").cells["CVE_ENT"].value[0]
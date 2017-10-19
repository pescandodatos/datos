#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv, os
from pathlib import Path
from difflib import SequenceMatcher
import unidecode

def reemplazar_acentos_enies(word):
    print(word)
    # reemplazar eñes
    new_word = word.replace("ñ", "n").replace("Ñ", "N")

    # reemplazar acentos
    return unidecode.unidecode(new_word)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def reemplazar_todo():
    files= ['beneficiarios_integral.csv', 'activos.csv','beneficiarios_componentes.csv','beneficiarios_diesel.csv','beneficiarios_motores.csv','solicitudes_men.csv','beneficiarios_pesca.csv','beneficiarios_gasolina.csv','beneficiarios_reconversion.csv','unidades.csv','beneficiarios_infraestructura.csv','embarcaciones_permisos.csv','permisos.csv', 'solicitudes_men.csv', 'solicitudes_may.csv']

    # write the encoded file
    for csv_file in files:
        print(csv_file)
        with open(csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames

            new_file = 'nuevos_datos/%s' % csv_file

            with open(new_file, 'w') as new_csvfile:
                writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader:
                    new_row = {}
                    for f in fieldnames:
                        new_row[f] = reemplazar_acentos_enies(row[f])
                    print(new_row) 
                    writer.writerow(new_row)

# Toma todas las bases y crea una sola para locations
def get_unique_localidades():
    
    location_file = 'localidades_nueva.csv'

    location_file_path = Path(os.join(os.getcwd(), location_file))
    if location_file_path.exists():
        return

    # get all CSV files
    files= ['beneficiarios_integral.csv', 'activos.csv','beneficiarios_componentes.csv','beneficiarios_diesel.csv','beneficiarios_motores.csv','solicitudes_men.csv','beneficiarios_pesca.csv','beneficiarios_gasolina.csv','beneficiarios_reconversion.csv','unidades.csv','beneficiarios_infraestructura.csv','embarcaciones_permisos.csv','permisos.csv', 'solicitudes_men.csv', 'solicitudes_may.csv']

    # beneficiarios_electricos.csv: text/plain; charset=us-ascii
    # beneficiarios_menores.csv: text/plain; charset=iso-8859-1
    # permisos_menores.csv: text/plain; charset=unknown-8bit
    # solicitudes_diesel.csv: text/plain; charset=us-ascii

    
    fieldnames = ['estado', 'municipio', 'localidad']

    with open(location_file, 'w') as new_csvfile:
        writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # write the encoded file
        for csv_file in files:
            print(csv_file)
            with open(csv_file, 'r') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    print(row)
                    new_row = {}
                    for f in fieldnames:
                        new_row[f] = row[f]
                    print(new_row) 
                    writer.writerow(new_row)


# Get unique estados, unique municipios, unique localidd

# Remplazaar estado.csv en localidad_nueva.csv
# Reemplazar municipio.csv
# Reemplazar localidad.csv

# CHECK LOCALIDADES WITH INEGI SIMILARITIES (transform it)


if __name__ == '__main__':
    reemplazar_todo()
    # get_unique_localidades()

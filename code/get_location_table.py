#!/usr/bin/python
# -*- coding: utf-8 -*-


# Toma todas las bases y crea una sola para locations

def main():
    # get all CSV files
    files=['beneficiarios_gasolina.csv']
#, beneficiarios_motores.csv               marginacion_localidad.csv               solicitudes_may.csv
# activo.csv                              beneficiarios_integral.csv              beneficiarios_reconversion.csv          marginacion_municipal.csv               solicitudes_men.csv
# beneficiarios_componentes.csv           beneficiarios_menores.csv               embarcacion.csv                         permiso.csv                             unidad_economica.csv
# beneficiarios_diesel.csv                beneficiarios_modernicacion_may.csv     inegi.csv                               solicitudes_diesel.csv
# beneficiarios_electricos.csv            beneficiarios_modernizacion_men.csv     marginacion.csv                         solicitudes_gasolina.csv
# ]

    location_file = 'location.csv'
    fieldnames = ['estado', 'municipio', 'localidad', 'cod_inegi']

    with open(location_file, 'w') as new_csvfile:
        
        writer = csv.DictWriter(newcsvfile, fieldnames=fieldnames)

        for csv_file in files:
            with open(csv_file, 'rb') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    new_row = {}
                    for f in fieldnames:
                        new_row[f] = row[f]
                    new_csvfile.write(new_row)

if __name__ == '__main__':
    main()

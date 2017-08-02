#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas

# PROCESO de unir las embarcaciones activas con las unidades economicas por el rnpa

# embarcaciones
# activos.csv
# RNPA_ACTIVO,NOMBRE_EMBARCACION,TIPO,MUNICIPIO,LOCALIDAD,ESTADO,ANO_CONSTRUCCION
# 60828

# unidades economicas
# unidades_economicas.csv
# TIPO,RNPA_UNIDAD_ECONOMICA,NOMBRE_UNIDAD_ECONOMICA,FECHA_REGISTRO,TIPO_PERSONA,REPRESENTANTE_LEGAL,ESTADO,MUNICIPIO,LOCALIDAD,INICIO
# 21258

# - nombre de la unidad economica: compañia donde esta registrado el rnpa
# - representante legal: persona que representa

# embarcaciones con sus unidades economicas
# embarcaciones.csv
# RNPA_ACTIVO,NOMBRE_EMBARCACION,RNPA_UNIDAD_ECONOMICA,NOMBRE_UNIDAD_ECONOMICA,ESTADO,MUNICIPIO,LOCALIDAD,TIPO_EMBARCACION,FECHA_REGISTRO
# 73548

def main():
    activos = pandas.read_csv('activos.csv')
    unidades_economicas = pandas.read_csv('unidades_economicas.csv')
    embarcaciones = pandas.read_csv('embarcaciones.csv')


    embarcaciones_activos = embarcaciones.merge(activos, how='left', on='RNPA_ACTIVO', left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('', '_a'), copy=True, indicator=False)
    new_embarcaciones = embarcaciones_activos.merge(unidades_economicas, how='left', on='RNPA_UNIDAD_ECONOMICA', left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('', '_ua'), copy=True, indicator=False)


    new_embarcaciones.to_csv('embarcaciones_detalles.csv', sep= ',', encoding='utf-8')


if __name__ == '__main__':
    main()
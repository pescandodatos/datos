# Get data
curl -o estados.zip http://mapserver.inegi.org.mx/MGN/mge2010v5_0.zip
curl -o  municipios.zip http://mapserver.inegi.org.mx/MGN/mgm2010v5_0.zip
unzip estados.zip 
unzip municipios.zip

# Convert into projection
ogr2ogr states.shp Entidades_2010_5.shp -t_srs "+proj=longlat +ellps=WGS84 +no_defs +towgs84=0,0,0"
ogr2ogr municipalities.shp Municipios_2010_5.shp -t_srs "+proj=longlat +ellps=WGS84 +no_defs +towgs84=0,0,0"

# Convert into geojson

ogr2ogr activos.geojson -select RNPA,Embarcacion,Tipo,Municipio,Localidad,Estado,Ano_Construido
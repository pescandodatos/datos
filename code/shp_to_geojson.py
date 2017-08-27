from osgeo import ogr
ds_fname = r'C:\Temp\countries.shp' # update this to your Shapefile
ds = ogr.Open(ds_fname)
if not ds:
    raise IOError('Could not open ' + ds_fname)
layer = ds.GetLayer()
for fid in range(layer.GetFeatureCount()):
    feat = layer.GetFeature(fid)
    json = feat.ExportToJson()
    # Only print the first 70 characters of GeoJSON output, since it can be long
    print('%3i : %s ...'%(fid, json[:80]))



 import shapefile
# read the shapefile
reader = shapefile.Reader("my.shp")
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature", \
    geometry=geom, properties=atr)) 

# write the GeoJSON file
from json import dumps
geojson = open("pyshp-demo.json", "w")
geojson.write(dumps({"type": "FeatureCollection",\
"features": buffer}, indent=2) + "\n")
geojson.close()


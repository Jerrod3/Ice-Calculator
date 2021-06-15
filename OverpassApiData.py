import requests
import json
from pyproj import Geod

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
(node["natural"="water"](45.148421, -93.133492,45.202695, -93.054006);
 way["natural"="water"](45.148421, -93.133492,45.202695, -93.054006);
 rel["natural"="water"](45.148421, -93.133492,45.202695, -93.054006);
);
out geom;
"""

#coordinates are counter clockwise

response = requests.get(overpass_url,
                        params={'data': overpass_query})
data = response.json()
Bigdict = {}
names = []
places = []
for dicts in data['elements']:
    parts = dicts.items()
    for key, value in parts:
        name = ''
        place = ''
        if key == "tags":
            a = value
            name = a.get("name")
            names.append(name)
        elif key == "geometry":
            coords = value
            perim = []
            for points in coords:
                lat = points.get('lat')
                lon = points.get('lon')
                perim.append([lat,lon])
            places.append(perim)
print(len(places))
amount = len(places)
count = 0
times = 0
for name in names:
    if name == None:
        name = "Nameless" + str(times)
        times = times + 1
    if amount == count:
        break
    else:
        Bigdict.update({name:(places[count])})
        count = count + 1
print(Bigdict.get("George Watch Lake"))

lats = []
lons = []
for values in Bigdict.get("George Watch Lake"):
    lat = values[0]
    lon = values[1]
    lats.append(lat)
    lons.append(lon)
# figure out what Geod param means
geod = Geod('+a=6378137 +f=0.0033528106647475126')

poly_area = (geod.polygon_area_perimeter(lons, lats))
print(poly_area)
if poly_area[0] < 0:
    poly_area = poly_area[0] * -1
print(poly_area)


# Need to adjust for lakes like spring lake, where multiple polys exist for same name
# Only works for way type objects, need to adjust for multi-polygons.
# Need to find ways to either get rid of nameless objects or find names

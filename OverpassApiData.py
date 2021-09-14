import requests
import json
from pyproj import Geod

overpass_url = "http://overpass-api.de/api/interpreter"
# The query is a textbox on a map, the first set is the southwest point, second is northeast
overpass_query = """
[out:json];
(node["natural"="water"](42.3253367, -85.4138615,42.3903357, -85.3537123);
 way["natural"="water"](42.3253367, -85.4138615,42.3903357, -85.3537123);
 rel["natural"="water"](42.3253367, -85.4138615,42.3903357, -85.3537123);
);
out geom;
"""

#coordinates are counter clockwise, nodes are points, ways are polygons, rels are multipolygons

response = requests.get(overpass_url,
                        params={'data': overpass_query})
data = response.json()
# Format the water polygons by name and waypoints. The waypoints represent points around the lake.
# I started by adding all the names of lakes to one list, then coords of each place to another.
# Then I format through those and add the names and locations into Bigdict by placing names as
# keys and places as values.
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
amount = len(places)
count = 0
times = 0
# Update the dictionary to name features without names to "nameless"
for name in names:
    if name == None:
        name = "Nameless" + str(times)
        times = times + 1
    if amount == count:
        break
    else:
        Bigdict.update({name:(places[count])})
        count = count + 1
# Format lats and lons for each lake so we can plug them into pyproj's area calculation. Maybe add this and
# area calcs into the same function?
lats = []
lons = []
all_lat_longs = {}
for key, value in Bigdict.items():
    lats = []
    lons = []
    for coords in value:
        lat = coords[0]
        lon = coords[1]
        lats.append(lat)
        lons.append(lon)
    all_lat_longs.update({key:(lats,lons)})

# Create a dictionary that contains lake names that are in square meters.
area_calcs = {}
geod = Geod(ellps = 'WGS84')
for key, value in all_lat_longs.items():
    poly_area = (geod.polygon_area_perimeter(value[1], value[0]))
    if poly_area[0] < 0:
        # If the area is negative, make it positive. This can happen if waypoints are reversed around the lake.
        poly_area = poly_area[0] * -1
        area_calcs.update({key:poly_area})


print(Bigdict)

# area in m^2. Judging from Sherman lake only, area calc 97% accurate from DNR estimate.
# Need to adjust for lakes like spring lake, where multiple polys exist for same name
# Only works for way type objects, need to adjust for multi-polygons.
# Need to find ways to either get rid of nameless objects or find names

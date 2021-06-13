import requests
import json

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
(node["natural"="water"](42.247293, -85.369165,42.440377, -85.156989);
 way["natural"="water"](42.247293, -85.369165,42.440377, -85.156989);
 rel["natural"="water"](42.247293, -85.369165,42.440377, -85.156989);
);
out geom;
"""

#coordinates are counter clockwise

response = requests.get(overpass_url,
                        params={'data': overpass_query})
data = response.json()
Bigdict = {}
for dicts in data['elements']:
    parts = dicts.items()
    for key, value in parts:
        name = ''
        perim = []
        place = ''
        if key == "tags":
            a = value
            name = a.get("name")
            place = type(name)
            if place == str:
                pass
            else:
                continue
        elif key == "geometry":
            coords = value
            for points in coords:
                lat = points.get('lat')
                lon = points.get('lon')
                perim.append([lat,lon])
        print(name)
        print(perim)
        Bigdict.update({name:perim})
print(Bigdict)

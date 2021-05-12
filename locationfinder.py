from geopy.geocoders import Nominatim
import geocoder
#Find the users coordinates
g = geocoder.ip('me')
usercords = (g.latlng)
#Use Geolocater to reverse geocode the coordinates for an address
geolocator = Nominatim(user_agent="Ice_calculator")
location = geolocator.reverse(usercords)
#Isolate the ZIP code to run against the database
user_location = location.address
chopped = user_location.split(',')
twozips = chopped[6]
pickfirst = twozips.split('-')
user_zip = pickfirst[0]

#import statements
import requests
import datetime
import numpy as np
import pandas as pd
import os
import sys
from geopy.geocoders import Nominatim
import geocoder

mytoken = "pXrEKHJMAIgWTJjjDbofqdYFJitWVAQp"

#Get 3 months prior
initdate = datetime.datetime.now()-datetime.timedelta(days=90)
#split the string to get an acceptable date value for NOAA
stringdate = str(initdate)
cutdate = stringdate.split()
begin_date = cutdate[0]
#today's date
end_date = (datetime.datetime.now().strftime('%Y-%m-%d'))

g = geocoder.ip('me')
usercords = (g.latlng)
#Use Geolocater to reverse geocode the coordinates for an address
geolocator = Nominatim(user_agent="Ice_calculator")
location = geolocator.reverse(usercords)
#Isolate the ZIP code to run against the database.
user_location = location.address
print(user_location)
chopped = user_location.split(',')
print(chopped)
nospace = []
for i in chopped :
    a = i.lstrip()
    print(a)
    nospace.append(a)
print(nospace)
ziponly = [x for x in nospace if x.isdigit()]
print(ziponly)

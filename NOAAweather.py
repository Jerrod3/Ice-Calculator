#import statements
import requests
import datetime
import numpy as np
import pandas as pd
import os
import sys
from geopy.geocoders import Nominatim
import geocoder
import sqlite3

mytoken = "pXrEKHJMAIgWTJjjDbofqdYFJitWVAQp"

#Get weather data from 3 months prior
initdate = datetime.datetime.now()-datetime.timedelta(days=90)
#split the string to get an acceptable date value for NOAA
stringdate = str(initdate)
cutdate = stringdate.split()
begin_date = cutdate[0]
#today's date
end_date = (datetime.datetime.now().strftime('%Y-%m-%d'))

g = geocoder.ip('me')
usercords = (g.latlng)
#Use Geolocater to reverse geocode the coordinates for an address,
#using IP to find location

geolocator = Nominatim(user_agent="Ice_calculator")
location = geolocator.reverse(usercords)
#Isolate the ZIP code to run against the database.
user_location = location.address
chopped = user_location.split(',')
nospace = []
for i in chopped :
    a = i.lstrip()
    nospace.append(a)
print(nospace)
ziponly = []
for scope in nospace :
    if scope == nospace[0] :
        continue
    place = scope[0].isdigit()
    if place == True :
        ziponly.append(scope)
        break
    else:
        continue
if any("-" in x for x in ziponly) :
    empty = ''
    whole = empty.join(ziponly)
    cut = whole.split("-")
    splitzip = whole[0]
    print(splitzip)
else:
    splitzip = ziponly[0]
print(splitzip)
#sometimes ziponly picks up on a number that is not the zip code, need to fix
user_zip = splitzip
print(user_zip)
cleanzip = "ZIP:" + user_zip
finalzip = cleanzip.strip('')
print(finalzip)
# See if the ZIP code is available for NOAA's daily value dataset (GHCND),
# otherwise, find the nearest ZIP code to plugin
conn = sqlite3.connect('zipdb.sqlite')
cur = conn.cursor()
def zip_finder(myzip):
    cur.execute("SELECT ZIP FROM ZIPS WHERE ZIP = (?) LIMIT 1", (myzip,))
    if cur.fetchone():
        print("ZIP in database")
        return myzip
    else:
        while True:
            ZIP = []
            for i in myzip :
                if i.isdigit() :
                    ZIP.append(i)
                else :
                    continue
            string = ''
            fork = int(string.join(ZIP))
            addone = fork + 1
            myzip = 'ZIP:' + str(addone)
            cur.execute("SELECT ZIP FROM ZIPS WHERE ZIP = (?) LIMIT 1", (myzip,))
            if cur.fetchone():
                print("found a match")
                return myzip
                break
            else :
                print("no match found, searching...")
                continue
print(zip_finder(finalzip))

locationid = "ZIP:00007"        #"ZIP:92101"  #zip_finder(finalzip)
print(locationid)
datasetid = 'GHCND' #datset id for "Daily Summaries"

base_url_data = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
base_url_stations = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'

def get_weather(locationid, datasetid, begin_date, end_date, mytoken, base_url):
    token = {'token': mytoken}

    #passing as string instead of dict because NOAA API does not like percent encoding
    params = 'datasetid='+str(datasetid)+'&'+'locationid='+str(locationid)+'&'+'startdate='+str(begin_date)+'&'+'enddate='+str(end_date)+'&'+'limit=1000'+'&'+'units=standard'

    r = requests.get(base_url, params = params, headers=token)
    print("Request status code: "+str(r.status_code))

    try:
        #results comes in json form. Convert to dataframe
        df = pd.DataFrame.from_dict(r.json()['results'])
        print("Successfully retrieved "+str(len(df['station'].unique()))+" stations")
        dates = pd.to_datetime(df['date'])
        print("Last date retrieved: "+str(dates.iloc[-1]))

        return df

    #Catch all exceptions for a bad request or missing data
    except:
        print("Error converting weather data to dataframe. Missing data?")

df_weather = get_weather(locationid, datasetid, begin_date, end_date, mytoken, base_url_data)
print(df_weather)

#Maybe turn this transformation of data into a function? Very ugly

compressed = df_weather[["date","datatype", "value"]]
plist = compressed.values.tolist()
rainfall = []
snowfall = []
groundsnow = []
tempmax = []
tempmin = []
windavg = []

for i in plist :
    if i[1] == 'PRCP' :
        rainfall.append(i)
    elif i[1] == 'SNOW' :
        snowfall.append(i)
    elif i[1] == 'SNWD' :
        groundsnow.append(i)
    elif i[1] == 'TMAX' :
        tempmax.append(i)
    elif i[1] == 'TMIN' :
        tempmin.append(i)
    elif i[1] == 'AWND' :
        windavg.append(i)
    else :
        continue
count_rain = 0
count_snow = 0
count_ground = 0
count_tmax = 0
count_tmin = 0
count_wind = 0
for i in rainfall :
    i.remove("PRCP")
    count_rain = count_rain + 1
    i[0] = count_rain
for i in snowfall :
    i.remove("SNOW")
    count_snow = count_snow + 1
    i[0] = count_snow
for i in groundsnow :
    i.remove("SNWD")
    count_ground = count_ground + 1
    i[0] = count_ground
for i in tempmax :
    i.remove("TMAX")
    count_tmax = count_tmax + 1
    i[0] = count_tmax
for i in tempmin :
    i.remove("TMIN")
    count_tmin = count_tmin + 1
    i[0] = count_tmin
for i in windavg :
    i.remove("AWND")
    count_wind = count_wind + 1
    i[0] = count_wind

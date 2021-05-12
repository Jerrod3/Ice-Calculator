#import statements
import requests
import datetime
import numpy as np
import pandas as pd
import os
import sys
from geopy.geocoders import Nominatim
import geocoder

mytoken = "your distinct token"

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
#Isolate the ZIP code to run against the database
user_location = location.address
chopped = user_location.split(',')
twozips = chopped[6]
pickfirst = twozips.split('-')
user_zip = pickfirst[0]
fork = str(user_zip)

#Location key for the region you are interested in (can be found on NOAA or requested as a different API as well)
locationid = 'ZIP:(fork)' #location id for Michigan
datasetid = 'GHCND' #datset id for "Daily Summaries"

base_url_data = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'
base_url_stations = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'

def get_weather(locationid, datasetid, begin_date, end_date, mytoken, base_url):
    token = {'token': mytoken}

    #passing as string instead of dict because NOAA API does not like percent encoding
    params = 'datasetid='+str(datasetid)+'&'+'locationid='+str(locationid)+'&'+'startdate='+str(begin_date)+'&'+'enddate='+str(end_date)+'&'+'limit=100'+'&'+'units=standard'

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
df_weather.head(100)
print(df_weather)

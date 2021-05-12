#import statements
import requests
import datetime
import numpy as np
import pandas as pd
import os
import sys

mytoken = "your distinct token"

lastyear = datetime.datetime.now()-datetime.timedelta(days=365)

#Use the same begin and end date for just one day's data. Format for the API request
begin_date = lastyear.strftime("2021-04-02")
end_date = lastyear.strftime("2021-04-04")

#Location key for the region you are interested in (can be found on NOAA or requested as a different API as well)
datasetid = 'GHCND' #datset id for "Daily Summaries"
locationcategoryid	= 'ZIP'
datacategoryid = 'THIC'

base_url_locations = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/locations'

def get_location(locationcategoryid, datasetid, datacategoryid, mytoken, base_url):
    token = {'token': mytoken}

    #passing as string instead of dict because NOAA API does not like percent encoding
    params = 'datacategoryid='+str(datacategoryid)+'&'+'locationcategoryid='+str(locationcategoryid)+'&'+'datasetid='+str(datasetid)+'&'+'startdate='+str(begin_date)+'&'+'enddate='+str(end_date)+'&'+'limit=1000'+'&'+'offset=11000'+'&'+'units=standard'

    r = requests.get(base_url, params = params, headers=token)
    print("Request status code: "+str(r.status_code))

    try:
        #results comes in json form. Convert to dataframe
        df = pd.DataFrame.from_dict(r.json()['results'])
        print("Successfully retrieved "+str(len(df['id'].unique()))+" locations")

        return df

    #Catch all exceptions for a bad request or missing data
    except:
        print("Error converting weather data to dataframe. Missing data?")

df_weather = get_location(locationcategoryid, datasetid, datacategoryid, mytoken, base_url_locations)
df_weather.head(1000)
print(df_weather)

#save as flattened csv
df_weather.to_csv('weather_'+str('round12')+'_noaa.csv', encoding='utf-8', index=False)

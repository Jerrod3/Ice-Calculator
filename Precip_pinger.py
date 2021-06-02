from NOAAweather import rainfall, snowfall, groundsnow, tempmax, tempmin, windavg

def countyboi(param):
    cumulative_inches = 0
    for tup in param:
        inches = tup[1]
        cumulative_inches = cumulative_inches + inches
    return cumulative_inches
cumulative_inches_snow = countyboi(snowfall)
cumulative_inches_rain = countyboi(rainfall)
snow_cover = countyboi(groundsnow)

def avgtemp(tempmax, tempin):
    Average = []
    DD = 0
    for x,n in zip(tempmax, tempin):
        Day = x[0]
        Max = x[1]
        print(Max)
        Min = n[1]
        print(Min)
        daily_DD = 32 - ((Max + Min)/2)
        Average.append(tuple((Day,daily_DD)))
        if daily_DD < 0 :
            daily_DD = 0
            print(daily_DD)
        else :
            DD = daily_DD + DD
            print(DD)
    return DD, Average
print(avgtemp(tempmax,tempmin))







# Need to get daily averages that build based on historical daily amounts
# Need to get lake data (possibly on front end)
# Need to re-route ZIP finder to go to next ZIP if no data is available

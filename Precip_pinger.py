from NOAAweather import rainfall, snowfall, groundsnow, tempmax, tempmin

print(rainfall)
print(snowfall)

cumlative_inches_rain = 0
cumulative_inches_snow = 0
for i in rainfall :
    cumlative_inches_rain = cumlative_inches_rain + int(i[1])

print(cumlative_inches_rain)

for i in snowfall :
    cumulative_inches_snow = cumulative_inches_snow + int(i[1])

print(cumulative_inches_snow)

print(groundsnow)

inst_snowcover = 0
for i in groundsnow :
    inst_snowcover = inst_snowcover + 1
try:
    current_snow_cover = groundsnow[(int(inst_snowcover))-1]
    if current_snow_cover > cumulative_inches_snow :
        cumulative_inches_snow = current_snow_cover
except:
    print("No snow values")

print(tempmax)
print(tempmin)

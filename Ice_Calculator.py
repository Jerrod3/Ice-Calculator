#Variables for parameters used in the loops below, used to calculate ice thicc#
countW = 0
countT = 0
DD = 0
Rain = 0
Snow = 0
AVGwind = 0
Windinches = 0
Covermult = 0
AVGTemp = 0
Tempinches = 0
Lake_Type = 0
FRain = 1
FSnow = 1
Ice = 0
Days = 0
#Current Ice cover#
while True :
    try:
        Ice = int(input("Current ice depth?"))
        break
    except:
        print("Please enter a valid ice depth")
        continue
while True :
    try:
        Days = int(input("How many days worth of conditions?"))
        break
    except:
        print("Please enter a valid number")
        continue
#Loop to calculate inches of ice created by wind and temperature with no ice present, and degree days over a selected span of time#
for i in range(Days) :
    if Ice > 0 :
        while True :
            try:
               highT = int(input("High?"))
               break
            except:
                print("Please enter a valid temperature")
                continue
        while True :
            try:
                lowT = int(input("Low?"))
                break
            except:
                print("Please enter a valid temperature")
                continue
        AVGDtemp = (32 -((highT + lowT)/2))
        if AVGDtemp < 0 :
            AVGDtemp = 0
        DD = DD + AVGDtemp
    elif Ice == 0 :
        while True :
            try:
                highT = int(input("High?"))
                break
            except:
                print("Please enter a valid temperature")
                continue
        while True:
            try:
                lowT = int(input("Low?"))
                break
            except:
                print("Please enter a valid temperature")
                continue
        while True:
            try:
                Hwind = int(input("High wind speed?"))
                break
            except:
                print("Please enter a valid wind speed")
                continue
        while True:
            try:
                Lwind = int(input("Low wind speed?"))
                break
            except:
                print("Please enter a valid wind speed")
                continue
        AVGDtemp = (32 -((highT + lowT)/2))
        if AVGDtemp < 0 :
            AVGDtemp = 0
        AVGDwind = (Hwind + Lwind)/2
        Windmath = AVGDwind * .018888 * AVGDtemp
        Tempmath = AVGDtemp * .047244
        Tempinches = Tempinches + Tempmath
        Windinches = Windinches + Windmath
print(DD)
print(Windinches)
print(Tempinches)
# Create an inverse relationship between lake depth and area?#
while True:
    try:
        Min = int(input("Depth Min?"))
        break
    except:
        print("Please enter a valid depth")
        continue
while True:
    try:
        Max = int(input("Depth Max?"))
        break
    except:
        print("Please enter a valid depth")
        continue
Depth = Max - Min
while True:
    try:
        Area = int(input("Lake Area?"))
        break
    except:
        print("Please enter a valid area")
        continue
Volume = Depth * Area
if Volume <= 300 :
    Lake_Type = 1
elif Volume >= 301 or Volume <= 600 :
    Lake_Type = .8
elif Volume >= 601 or Volume <= 1000 :
    Lake_Type = .6
else :
    Lake_Type = .5
#Loop to calculate ice cover created by clear weather conditions over a selected span of time#
for i in range(Days) :
#Stuck in infinite loop currently
    cover = None
    while True :
        cover = input("cloudy or clear?")
        print(cover)
        if cover == "clear" :
            cover = 1
            break
        elif cover == "cloudy" :
            cover = 0
            break
        else :
            print("Please enter a valid cover choice")
            continue
    if cover == 1 :
        cover = .6614173
    else :
        cover = 0
    Covermult = Covermult + cover
print(cover)
print(Covermult)
#Arbitrary relationship established for practice, need to find actual relationship between rain and ice cover
for i in range(Days) :
    while True :
        try:
            init_rain = int(input("Inches of rain?"))
            break
        except:
            print("Please enter a valid amount of precipitation")
            continue
    Rain = init_rain + Rain
    if Rain == 0 :
        Rain = 1
    print(Rain)
    FRain = 1/Rain
    if FRain < .33 :
        FRain = .33
    print(FRain)
#Arbitrary relationship established for practice, need to find actual relationship between snow and ice cover
for i in range(Days) :
    while True :
        try:
            init_snow = int(input("Inches of snow?"))
            break
        except:
            print("Please enter a valid amount of precipitation")
            continue
    Snow = init_snow + Snow
    if Snow == 0 :
        Snow = 1
    FSnow = 1/Snow
    if FSnow < .33 :
        FSnow = .33
#If statement used to select the proper equation for the given situation (initial ice cover)#
#Last equation is converting the constants from mm to in/day, wind(fixed) and Temp#
#loop is currently based on averages over the days specified. This is iinaccurate#
if Ice > 0 :
    IceD = Lake_Type * FSnow * FRain *(Ice + (DD * .06666667))
elif Ice <= 0 :
    IceD = Lake_Type * FSnow * FRain * (Covermult + Windinches + Tempinches)
print(IceD)

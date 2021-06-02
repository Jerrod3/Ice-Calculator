# Data needed: LATDD83(36), LONDD83(37),Elevation(18) SIZE_CLASS, EVAL_NAME(30),AREACLS, AREA_HA(13)

with open("EPA.txt") as c :
    Data = [line.rstrip("/n") for line in c]
Chunked_data = []
for sett in Data :
    component = sett.split(",")
    chonk = []
    for piece in component :
        chonk.append([piece])
    Chunked_data.append(chonk)
latlong = []
for i in Chunked_data :
    for a in i[36] :
        for b in a[1] :
            try:
                check = int(b)
                latlong.append(tuple((i[13],i[18],i[30],i[36],i[37])))
            except :
                latlong.append(tuple((i[14],i[19],i[31],i[37],i[38])))
                continue
print(len(latlong))

#later on, use these coordinates to match up with javascript location

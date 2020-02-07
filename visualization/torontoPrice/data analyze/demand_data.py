import time
import numpy as np

np.set_printoptions(suppress=True)

#print(time.time()*1000)
now = 1392176000000#int(round(time.time()*1000))
now02 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
print("1",now)
print(now02)
format_time = '2017-10-16 18:22:06'
ts = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
test = time.mktime(ts)*1000
now03 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(test/1000))
print(now03)
def get_time(time_in):
    format_time = time_in
    timestamp = []
    string = 'abcdafg'
    newstr = string.replace('a', 'e')
    print(string, newstr)
    time_string=['0','1','2','3','4','5','6','7']
    for i in time_string:
        newtime = format_time.replace('7',i)
        ts = time.strptime(newtime, "%Y-%m-%d %H:%M:%S")
        newtime = time.mktime(ts) * 1000
        timestamp.append(newtime)
    timestamp = [timestamp]
    return  timestamp
get_time(format_time)

house = [[1287267726000,899],[1318803726000,1345],[1350426126000,1105],[1381962126000,1593],[1413498126000,2683],[1445034126000,2965],[1476656526000,3450],[1508192526000,3798]]
townhouse = [[1287267726000,665],[1318803726000,830],[1350426126000,885],[1381962126000,1209],[1413498126000,1673],[1445034126000,1532],[1476656526000,1425],[1508192526000,1687]]
condo = [[1287267726000,1345],[1318803726000,1502],[1350426126000,1059],[1381962126000,1328],[1413498126000,1509],[1445034126000,1892],[1476656526000,1992],[1508192526000,1675]]
total = []
total.append(house)
total.append(townhouse)
total.append(condo)
#house = np.concatenate((timestamp,house), axis=0)
#house = np.asarray(house)
#print(house.shape)
#house = np.stack(house,axis = 1)

print("house",house)
#townhouse = np.concatenate((timestamp,townhouse), axis=0)
#townhouse = np.stack(townhouse,axis = 1)
print("townhouse",townhouse)
#condo = np.concatenate((timestamp,condo), axis=0)
#ondo = np.stack(condo,axis = 1)

print("condo",condo)
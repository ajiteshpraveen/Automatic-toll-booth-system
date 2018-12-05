import datetime
from datetime import timedelta
now = datetime.datetime.now()

print (now.strftime("%Y-%m-%d %H:%M:%S"))
t2 = now.strftime("%Y-%m-%d %H:%M:%S")
FMT = '%Y-%m-%d %H:%M:%S'
t = '2018-10-21 01:11:12'
tdelta = now.strptime(t2, FMT) - now.strptime(t, FMT)
print(tdelta)
print("Days")
print(tdelta.days)
print("Seconds")
print(tdelta.seconds)


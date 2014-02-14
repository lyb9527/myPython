import time
import datetime

#print(time.time())
#print(time.clock())
#print(time.gmtime())
#print(time.localtime())
#print(time.mktime(time.localtime()))
#print(datetime.datetime(2013,12,9,14,42))

t      = datetime.datetime(2012,9,3,21,30)
t_next = datetime.datetime(2012,9,5,23,30)
delta1 = datetime.timedelta(seconds = 600)
delta2 = datetime.timedelta(weeks = 3)
print(t + delta1)
print(t + delta2)
print(t_next - t)
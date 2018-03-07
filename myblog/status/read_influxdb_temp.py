#import time
from influxdb import InfluxDBClient

s = 'xiqidongshu_test'
q="select * from temperature where client=" + "\'"+s+"\'" + " order by time desc limit 10"
client = InfluxDBClient('111.47.20.166', 8086, 'admin', '', 'terminals')
#result = client.query("select * from temperature where client='gxgadzt' order by time desc limit 10")
result = client.query(q)
#print result
for r in result:
    #print r
    for t in r:
        utc_time = t['time']
        diff = int(utc_time[11:13])+8
        if diff >= 24:
            local_hour = diff - 24
        else:
            local_hour = diff
        replace = str(local_hour)
        local_time = utc_time[:11] + replace + utc_time[13:]
        print("Client: %s; Temperature: %s; Time: %s" % (t['client'], t['tempdata'], local_time))
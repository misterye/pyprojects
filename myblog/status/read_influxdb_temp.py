#import time
from influxdb import InfluxDBClient

s = 'gxgadzt'
q="select * from temperature where client=" + "\'"+s+"\'" + " order by time desc limit 10"
client = InfluxDBClient('localhost', 8086, 'admin', '', 'terminals')
#result = client.query("select * from temperature where client='gxgadzt' order by time desc limit 10")
result = client.query(q)
#print result
for r in result:
    #print r
    for t in r:
        print("Client: %s; Temperature: %s; Time: %s" % (t['client'], t['tempdata'], t['time']))
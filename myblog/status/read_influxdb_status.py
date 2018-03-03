#import time
from influxdb import InfluxDBClient

s = '10.8.0.15'
q="select * from status where ip=" + "\'"+s+"\'" + " order by time desc limit 10"
#q=("""select * from status where ip="{s}" order by time desc limit 10""").format(s='10.8.0.15')
client = InfluxDBClient('localhost', 8086, 'admin', '', 'terminals')
result = client.query(q)
if result:
    #print result
    for r in result:
        #print r
        for t in r:
            print("IP: %s; Connection Status: %s; Time: %s" % (t['ip'], t['connect'], t['time']))
else:
    print "No Client."

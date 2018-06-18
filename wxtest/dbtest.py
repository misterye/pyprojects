from influxdb import InfluxDBClient

influxclient = InfluxDBClient('111.47.20.166', 8086, 'admin', '', 'telegraf')
client_name = 'gxgadzt'
qstatus = "select value from mqtt_consumer where topic=" + "\'devices/raspi/"+client_name+"/status\'" + " order by time desc limit 1"
statusresult = influxclient.query(qstatus)
if statusresult:
	conn_stat = 'on'
else:
	conn_stat = 'off'
print conn_stat

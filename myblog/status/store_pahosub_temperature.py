import time
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

def on_message(client, userdata, message):
    clientstr = message.topic.split('/')[2]
    print clientstr
    print message.payload
    influxclient = InfluxDBClient('111.47.20.166', 8086, 'admin', '', 'terminals')
    json_body = [
        {
            "measurement": "temperature",
            "fields": {
                "client": clientstr,
                "tempdata": message.payload
            }
        }
    ]
    influxclient.write_points(json_body)

broker = '111.47.20.166'
while True:
    client = mqtt.Client("serversub")
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.loop_start()
    client.subscribe('devices/raspi/#')
    time.sleep(4)
    client.loop_stop()
    client.disconnect()
    time.sleep(1)

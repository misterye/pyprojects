import time
import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    #print message.payload
    print("message received: ", message.payload)
    print("message topic: ", message.topic)
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #print("message qos: ", message.qos)
    #print("message retain flag: ", message.retain)


broker = '111.47.20.166'
while True:
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.loop_start()
    client.subscribe('devices/raspi/#')
    time.sleep(4)
    client.loop_stop()
    client.disconnect()
    time.sleep(2)

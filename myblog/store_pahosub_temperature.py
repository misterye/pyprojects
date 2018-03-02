import time
import paho.mqtt.client as mqtt
import MySQLdb

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker.")
        global Connected
        Connected = True
    else:
        print("Connection failed.")

def on_message(client, userdata, message):
    try:
        clientstr = message.topic.split('/')[2]
        db = MySQLdb.connect(host='localhost', user='root', passwd='840821', db='myblog')
        cur = db.cursor()
        print "Storing client temperature data ..."
        sql = ("""INSERT INTO temperature (tempdata, client) VALUES (%s, %s)""", (message.payload, clientstr))
        #sql = ("""INSERT INTO temperature (data) VALUES (%s)""", [message.payload])
        cur.execute(*sql)
        db.commit()
        print "Done!"
    except:
        db.rollback()
        print "Operation failed!"
    cur.close()
    print clientstr + ": " + message.payload

broker = '111.47.20.166'
Connected = False
client = mqtt.Client("serversub")
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883, 60)
client.loop_start()
while Connected != True:
    time.sleep(0.1)
client.subscribe('devices/raspi/#')
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print "exiting..."
    cur.close()
    client.disconnect()
    client.loop_stop()

import requests
import os
import MySQLdb

os.system('/opt/vc/bin/vcgencmd measure_temp > /home/pi/Scripts/temp_log.log')

db = MySQLdb.connect(host="localhost", user="root", passwd="", db="templog")
cur = db.cursor()

with open('/home/pi/Scripts/temp_log.log','r') as templog:
    temp = templog.readline()

newtemp = temp[5:9]
print newtemp
sql = ("""INSERT INTO temptab (temperature) VALUES (%s)""", [newtemp])
try:
    print "Writing temperature to database..."
    cur.execute(*sql)
    db.commit()
    print "Write complete."
except:
    db.rollback()
    print "Writing temperature to database failed."

# post temperature json to server
data_from_pi = {'pi_temp':newtemp}
print data_from_pi
response = requests.post('http://139.224.114.83:8086/getTemp', json=data_from_pi)
if response.ok:
	print 'ok'
else:
	print 'Request post to server failed.'

cur.close()
db.close()
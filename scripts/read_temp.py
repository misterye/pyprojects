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

cur.close()
db.close()
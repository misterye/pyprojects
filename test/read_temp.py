import os
from time import sleep
import MySQLdb

db = MySQLdb.connect(host="localhost", user="root", passwd="840821", db="test")
cur = db.cursor()
print cur
newtemp = 35.9
try:
    print "Writing temperature to database..."
    cur.execute("""INSERT INTO temptab (temperature) VALUES (%s)""", [newtemp])
    db.commit()
    print "Write complete."
except:
    db.rollback()
    print "Writing temperature to database failed."

cur.close()
db.close()
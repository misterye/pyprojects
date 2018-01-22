import os
import MySQLdb
from time import sleep

while True:

    db = MySQLdb.connect(host="localhost", user="root", passwd="840821", db="myblog")
    cur = db.cursor()

    sql = ("DELETE FROM temperature WHERE create_time < NOW() - INTERVAL 10 DAY")
    #id = 1
    #sql = ("""SELECT * FROM status WHERE id=%s""", [id])
    try:
        print "Deleting temperature data more than ten days from table myblog.temperature..."
        cur.execute(sql)
        #cur.execute("""SELECT * FROM status WHERE id=1""")
        #cur.execute("""DELETE FROM status WHERE TO_DAYS(NOW())-TO_DAYS(time)>1""")
        db.commit()
        print "Delete complete."
    except:
        db.rollback()
        print "Delete temperature data more than ten days from table myblog.temperature failed."

    cur.close()
    db.close()
    sleep(864000)

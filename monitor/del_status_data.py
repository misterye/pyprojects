import os
import MySQLdb
from time import sleep

while True:

    db = MySQLdb.connect(host="localhost", user="root", passwd="840821", db="myblog")
    cur = db.cursor()

    #sql = ("""DELETE FROM status WHERE TO_DAYS(NOW())-TO_DAYS(time)>1""")
    #id = 1
    #sql = ("""SELECT * FROM status WHERE id=%s""", [id])
    try:
        print "Deleting data more than one day from table myblog.status..."
        #cur.execute(*sql)
        #cur.execute("""SELECT * FROM status WHERE id=1""")
        cur.execute("""DELETE FROM status WHERE TO_DAYS(NOW())-TO_DAYS(time)>1""")
        db.commit()
        print "Delete complete."
    except:
        db.rollback()
        print "Delete data more than one day from table myblog.status failed."

    cur.close()
    db.close()
    sleep(86400)

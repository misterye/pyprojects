# Filename: TwistedBeatServer.py

"""Asynchronous events-based heartbeat server"""

UDP_PORT = 43278; CHECK_PERIOD = 20; CHECK_TIMEOUT = 15

import time
from time import sleep
from twisted.application import internet, service
from twisted.internet import protocol
from twisted.python import log
import MySQLdb

class Receiver(protocol.DatagramProtocol):
    """Receive UDP packets and log them in the clients dictionary"""

    def datagramReceived(self, data, (ip, port)):
        if data == 'PyHB':
            self.callback(ip)

class DetectorService(internet.TimerService):
    """Detect clients not sending heartbeats for too long"""

    def __init__(self):
        internet.TimerService.__init__(self, CHECK_PERIOD, self.detect)
        self.beats = {}

    def update(self, ip):
        self.beats[ip] = time.time()

    def detect(self):
        """Log a list of clients with heartbeat older than CHECK_TIMEOUT"""
        limit = time.time() - CHECK_TIMEOUT
        #silent = [ip for (ip, ipTime) in self.beats.items() if ipTime < limit]
        online = [ip for (ip, ipTime) in self.beats.items() if ipTime > limit]
        db = MySQLdb.connect(host='localhost', user='root', passwd='840821', db='myblog')
        cur = db.cursor()
        try:
            print "Getting all the clients ..."
            cur.execute("""SELECT client, ip FROM terminals""")
            data = cur.fetchall()
            print data
            clients = {}
            for d in data:
                clients[d[1]] = d[0]
            print clients
            ips = []
            for d in data:
                ips.append(d[1])
            print ips
        except:
            db.rollback()
            print "Operation failed!"
        on = 'on'
        off = 'off'
        for client in ips:
            if client in online:
                try:
                    print "Storing online client's status..."
                    sql = ("""INSERT INTO status (client, connect) VALUES (%s, %s)""", (clients[client], on))
                    cur.execute(*sql)
                    db.commit()
                    print "Done!"
                except:
                    db.rollback()
                    print "Operation failed!"
            else:
                try:
                    print "Storing offline client's status..."
                    sql = ("""INSERT INTO status (client, connect) VALUES (%s, %s)""", (clients[client], off))
                    cur.execute(*sql)
                    db.commit()
                    print "Done!"
                except:
                    db.rollback()
                    print "Operation failed!"
        cur.close()
        #log.msg('Beats items: %s' % self.beats)
        #log.msg('Silent clients: %s' % silent)
        log.msg('Online clients: %s' % online)

application = service.Application('Heartbeat')
# define and link the silent clients' detector service
detectorSvc = DetectorService()
detectorSvc.setServiceParent(application)
# create an instance of the Receiver protocol, and give it the callback
receiver = Receiver()
receiver.callback = detectorSvc.update
# define and link the UDP server service, passing the receiver in
udpServer = internet.UDPServer(UDP_PORT, receiver)
udpServer.setServiceParent(application)
# each service is started automatically by Twisted at launch time
log.msg('Asynchronous heartbeat server listening on port %d\n'
    'press Ctrl-C to stop\n' % UDP_PORT)

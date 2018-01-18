import urllib2
import requests

urlstr = urllib2.urlopen("http://satelc.com:5000/client_status")
print urlstr
#urlstr_content = urllib2.urlopen("http://satelc.com:5000/client_status").read()
#print urlstr_content

link = "http://satelc.com:5000/client_status"
r = requests.request("GET", link)
url = r.url
print url
#print r.headers

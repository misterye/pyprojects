#coding:utf-8
import requests

try:
    #response = requests.post('https://api.smsglobal.com/http-api.php?action=sendsms&user=tekffo9u&password=kjEAgNHz&&from=8613916838729&to=8613916838729&text=Hello%20world')
    response = requests.post('https://api.clockworksms.com/http/send.aspx?key=428ffed46c979990ec456a6687fe671f6b601fa1&to=8613764736209&content=Hello+World')
except requests.RequestException as e:
    print(e.message)

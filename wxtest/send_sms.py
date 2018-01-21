#coding:utf-8
import requests

try:
    response = requests.post('https://api.smsglobal.com/http-api.php?action=sendsms&user=tekffo9u&password=kjEAgNHz&&from=8613916838729&to=8613916838729&text=Hello%20world')
except requests.RequestException as e:
    print(e.message)

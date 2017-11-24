import requests
import os
from time import sleep

#while True:
for i in range(10):
    data_from_pi = {'pi_temp':37.5}
    response = requests.post('http://139.224.114.83:8022/getTemp', json=data_from_pi)
    if response.ok:
        print(response.json())
    sleep(5)



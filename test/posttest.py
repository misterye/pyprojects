import requests

data_from_pi = {'pi_temp':'25.3', 'pi_name':'gxgadzt'} 
try:
    response = requests.post('http://139.224.114.83:8019/getTemp', json=data_from_pi)
except requests.RequestException as e:
    print(e.message)

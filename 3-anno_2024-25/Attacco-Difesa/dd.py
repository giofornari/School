import requests


response = requests.get("http://10.254.0.1/api/client/attack_data/")
print(response.text)
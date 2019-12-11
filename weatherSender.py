import requests
import json
import os

location = ""
recipient = ""

# curl wttr.in/Durham_NH?1

response = requests.get("http://wttr.in/" + location + "?format=j1")

data = response.json()

# currentTemp = data["current_condition"][0]["temp_F"]
all = data["current_condition"][0]
# # next = data["current_condition"][1]

print(all)
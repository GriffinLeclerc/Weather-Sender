import requests
import json
import os

# A typical JSON response from http://wttr.in/

# {'FeelsLikeC': '1', 
# 'FeelsLikeF': '33', 
# 'cloudcover': '25', 
# 'humidity': '78', 
# 'observation_time': '03:37 AM', 
# 'precipMM': '0.0', 'pressure': '1034', 
# 'temp_C': '1', 
# 'temp_F': '33', 
# 'uvIndex': 1, 
# 'visibility': '16', 
# 'weatherCode': '116', 
# 'weatherDesc': [{'value': 'Partly cloudy'}], 
# 'weatherIconUrl': [{'value': ''}], 
# 'winddir16Point': 'N', 
# 'winddirDegree': '0', 
# 'windspeedKmph': '0', 
# 'windspeedMiles': '0'}

# Location you want the weather from
location = "Durham_NH"
# address to send this report to
recipient = ""

response = requests.get("http://wttr.in/" + location + "?format=j1")

data = response.json()

current_condition = data["current_condition"][0]

currentTempF = current_condition["temp_F"]
feelsLikeF = current_condition["FeelsLikeF"]
condition = current_condition["weatherDesc"][0]["value"]
windCompass = current_condition["winddir16Point"]
windSpeedMPH = current_condition["windspeedMiles"]

message = \
"Currently " + currentTempF + " degrees" + "\n" + \
"Feels Like " + feelsLikeF + " degrees" + "\n" + \
condition + "\n" + \
"Winds " + windCompass + " at " + windSpeedMPH + " MPH"

print(message)
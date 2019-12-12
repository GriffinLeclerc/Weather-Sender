import requests
import json
import os

IndexToNiceTime = {0: " in the morning", 1: " at noon", 2: " in the evening", 3: " at night"}

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

# if you live in a place where temperature is > 999 degrees
# or < -999 degrees
# results may be inaccurate
highTempF = -999
highTime = "never"

lowTempF = 999
lowTime = "never"

rainChance = 0
snowChance = 0

for i in range (4):
    temp = int(data["weather"][0]["hourly"][i]["tempF"])
    rain = int(data["weather"][0]["hourly"][i]["chanceofrain"])
    snow = int(data["weather"][0]["hourly"][i]["chanceofsnow"])

    if temp > highTempF:
        highTempF = temp
        highTime = IndexToNiceTime[i]
    elif temp < lowTempF:
        lowTempF = temp
        lowTime = IndexToNiceTime[i]

    if rain > snowChance:
        precipChance = rain
    if snow > snowChance:
        snowChance = snow

message = \
"Currently " + currentTempF + " degrees" + "\n" + \
"Feels Like " + feelsLikeF + " degrees" + "\n" + \
condition + "\n" + \
"Winds " + windCompass + " at " + windSpeedMPH + " MPH" + "\n" + \
"\n" + \
"High of " + str(highTempF) + highTime + "\n" + \
"Low of " + str(lowTempF) + lowTime

if rainChance > 0:
    message += "\n" + str(rainChance) + "% chance of rain"
if snowChance > 0:
    message += "\n" + str(snowChance) + "% chance of snow"

print(message)
import requests
import json
import os
import smtplib

def checkDailyChance(property):
    maxProperty = 0
    startTime = 0

    for i in range(8):
        hourlyProperty = int(data["weather"][0]["hourly"][i][property])
        time = int(data["weather"][0]["hourly"][i]["time"])

        if hourlyProperty > maxProperty:
            maxProperty = hourlyProperty
            if startTime == 0:
                startTime = time;

    return (maxProperty, startTime)

def getCivilianTime(militaryTime):
    time = str(int((militaryTime % 1200) / 100))
    if militaryTime > 1200:
        time += " PM"
    else:
        time += " AM"
    return time

# Location you want the weather from
location = ""
url = "http://wttr.in/" + location + "?format=j1"

# address you want the message sent from
# to protect those using this script, email address and password are gathered from environment variables
# please add these two environemnt variables with your corresponding contents, rather than storing your credentials in plain text
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASS")

# address to send this report to
recipient = ""

# mailserver to send your request to, default to gmail
mailServer = "smtp.gmail.com"
port = 587

IndexToNiceTime = {0: " in the morning", 1: " at noon", 2: " in the evening", 3: " at night"}

# Get the weather data
response = requests.get(url)

if response.status_code != 200:
    print("Unable to reach " + url + ". Error code: " + response.status_code)

data = response.json()

current_condition = data["current_condition"][0]
currentTempF = current_condition["temp_F"]
feelsLikeF = current_condition["FeelsLikeF"]
condition = current_condition["weatherDesc"][0]["value"]
windCompass = current_condition["winddir16Point"]
windSpeedMPH = current_condition["windspeedMiles"]
highTempF = data["weather"][0]["maxtempF"]
lowTempF = data["weather"][0]["mintempF"]

message = \
"Currently " + currentTempF + " degrees" + "\n" + \
"Feels Like " + feelsLikeF + " degrees" + "\n" + \
condition + "\n" + \
"Winds " + windCompass + " at " + windSpeedMPH + " MPH" + "\n" + \
"\n" + \
"High of " + str(highTempF)+ "\n" + \
"Low of " + str(lowTempF)

# Daily precipitation chances
rainData = checkDailyChance("chanceofrain")
rainChance = rainData[0]
rainTime = rainData[1]

snowData = checkDailyChance("chanceofsnow")
snowChance = snowData[0]
snowTime = snowData[1]

frostData = checkDailyChance("chanceoffrost")
frostChance = frostData[0]
frostTime = frostData[1]

if rainChance > 0:
    message += "\n" + str(rainChance) + "% chance of rain starting at " + getCivilianTime(rainTime)
if snowChance > 0:
    message += "\n" + str(snowChance) + "% chance of snow starting at " + getCivilianTime(snowTime)
if frostChance > 0:
    message += "\n" + str(frostChance) + "% chance of frost starting at " + getCivilianTime(frostTime)

with smtplib.SMTP(mailServer, port) as smtp:
    try:
        smtp.starttls()
        smtp.login(email_address, email_password)

        smtp.sendmail(email_address, recipient, message)
    except Exception as e:
        print("Unable to send message: " + str(e))
        print("Please ensure your credentials are correct. Such as desired email server and recipient address.")
        print("Also ensure you have system environment variables EMAIL_ADDRESS and EMAIL_PASS set accordingly.")
import requests
import json
import os
import smtplib
import configparser
import time

# address you want the message sent from
# to protect those using this script, email address and password are gathered from environment variables
# please add these two environemnt variables with your corresponding contents, 
# rather than storing your credentials in plain text in this script
email_address = os.environ.get("EMAIL_ADDRESS")
email_password = os.environ.get("EMAIL_PASS")

config = configparser.ConfigParser()
config.read('config.ini')

# Location you want the weather from
location = config["Weather"]["location"]
url = "http://wttr.in/" + location + "?format=j1"

# address to send this report to
recipient = config["Message"]["recipient"]

# mailserver to send your request to, default to gmail
mailServer = config["Message"]["mail_server"]
port = config["Message"]["port"]

def dailyPrecipitationChance(jsonProperty, propertyName):
    maxProperty = 0
    startTime = 0

    for i in range(8):
        hourlyProperty = int(data["weather"][0]["hourly"][i][jsonProperty])
        time = int(data["weather"][0]["hourly"][i]["time"])

        if hourlyProperty > maxProperty:
            maxProperty = hourlyProperty
            if startTime == 0:
                startTime = time;

    if maxProperty > 0:
        return (str(maxProperty) + "% chance of " + propertyName + " starting at " + getCivilianTime(startTime))
    return ""

def getCivilianTime(militaryTime):
    time = str(int((militaryTime % 1200) / 100))
    if militaryTime > 1200:
        time += " PM"
    else:
        time += " AM"
    return time

def sendMessage(message):
    with smtplib.SMTP(mailServer, port) as smtp:
        try:
            smtp.starttls()
            smtp.login(email_address, email_password)

            smtp.sendmail(email_address, recipient, message)

            smtp.quit()
        except Exception as e:
            print("Unable to send message: " + str(e))
            print("Please ensure your configuration file is correct.")
            print("Also ensure you have system environment variables EMAIL_ADDRESS and EMAIL_PASS set accordingly.")

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

currentConditions = \
"Currently " + currentTempF + " degrees" + "\n" + \
"Feels Like " + feelsLikeF + " degrees" + "\n" + \
condition + "\n" + \
"Winds " + windCompass + " at " + windSpeedMPH + " MPH" + "\n" + \
"\n" + \
"High of " + str(highTempF) + "\n" + \
"Low of " + str(lowTempF)

# Daily precipitation chances
dailyChances = (\
dailyPrecipitationChance("chanceofrain", "rain") + "\n" + \
dailyPrecipitationChance("chanceofsnow", "snow") + "\n" + \
dailyPrecipitationChance("chanceoffog", "fog")).strip()

# Send the created messages
sendMessage(currentConditions)
# The current conditions message is (on average) more characters than
# the precipitations message. Meaning, reguardless of order sent, mail servers will
# more quickly process and forward the daily chances message THEN forward the current 
# conditions message.
# Because the messages should be received in the opposite order, the script
# waits 1 second to give the servers time to forward the first message.
time.sleep(1)

sendMessage(dailyChances)
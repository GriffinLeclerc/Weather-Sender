import configparser
from pathlib import Path

if Path('config.ini').is_file():
    print("Configuration file already exists.")
    exit(-1)

config = configparser.ConfigParser()

config['Weather'] = {
    'location': 'none'
}

config['Message'] = {
    'recipient': 'none',
    'mail_server': 'smtp.gmail.com',
    'port': '587'
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)
### Weather Sender ###

This is a simple python script that sends a plain text message containing information about the weather over email.

## Usage ##

The script relies on two system environment variables: <br />
```
EMAIL_ADDRESS
EMAIL_PASS
```
These environment variables are used for secure email server login. <br />
Please take a moment to set these environment variables to their corresponding values. <br />
While you can store your credentials in the script, it is not recommended. <br />
<br />
Additionally, you will need to fill in the following configuration values. <br />
```
location = 
recipient = 
mailServer = smtp.gmail.com
port = 587 
```
Where: <br />
location is where you wish to see the weather reported from. <br />
recipient is where you wish to send the generated message. <br />
mailServer is the email server you wish to log into. Defaults to smtp.gmail.com. <br />
port is the port of the email server you wish to connect to. Defaults to 587. <br />

## Required Packages and Components ##
python3 <br />
the ability to reach [wttr.in]{https://wttr.in} <br />
an email address

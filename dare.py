#!/usr/bin/env python3

import urllib.request
import sys
import time
import json
import smtplib
from email.mime.text import MIMEText
from config import *

# Check if a commit has been made yesterday. If it has, congratulate. If not, swear.
def has_committed(user):
	with urllib.request.urlopen('https://api.github.com/users/' + user + '/events') as response:
		html = response.read().decode("utf-8")
           
		data = json.loads(html)

		yesterday = int(time.strftime("%d")) - 1 
		yesterdate = time.strftime("%Y-%m-") + str(yesterday)

		for event in data:
			if (event["type"] == "PushEvent" or event['type'] == "CreateEvent") and event['created_at'][:10] == yesterdate:
				return True

		return False

# Send an email to the recipient using the local server
def mail(user):
	msg = MIMEText(user + " has dared not to commit daily!")
	msg["Subject"] = "Dare violation!"
	msg["From"] = FROM
	msg["To"] = RECIPIENT

	s = smtplib.SMTP("localhost")
	s.send_message(msg)
	s.quit()

	print("[" +  time.strftime("%Y-%m-%d_%H:%M:%S") + "] Mail sent for user " + user)

# If the user has not committed, send an email to the recipient
def verify(user):
    if not has_committed(user):
        mail(user)

# This must be run with the username of the user to be checked as an argument
if __name__ == "__main__":
    for user in USER:
    	verify(user)

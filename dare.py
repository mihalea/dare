#!/usr/bin/env python3

import urllib.request
import sys
import time
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.text import MIMEText
from config import *

# Check if a commit has been made yesterday. If it has, congratulate. If not, swear.
def has_committed(user):
	with urllib.request.urlopen('https://api.github.com/users/' + user + '/events') as response:
		html = response.read().decode("utf-8")
           
		data = json.loads(html)

		yesterday = datetime.today() - timedelta(days=1)
		yesterdate = yesterday.strftime("%Y-%m-%d")

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

	log("Mail has been sent for user " + user)

# Log message to the std output
def log(msg):
	print("[" +  time.strftime("%Y-%m-%d_%H:%M:%S") + "] " + msg)

# If the user has not committed, send an email to the recipient
def verify(user):
	if not has_committed(user):
		mail(user)
	else:
		log("User " + user + " has committed lately")	
	

# This must be run with the username of the user to be checked as an argument
if __name__ == "__main__":
    for user in USER:
    	verify(user)

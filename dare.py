#!/usr/bin/env python3

import urllib.request
import sys
import time
import json
import smtplib
from email.mime.text import MIMEText
from config import *

class DoesNotCount(Exception):
    pass

# Get the last commit's date for $user as a string formatted as follows: %Y-%m-%dT%HH:%mm:%ssZ
def get_last_commit_date(user):
    with urllib.request.urlopen('https://api.github.com/users/' + user + '/events') as response:
           html = response.read().decode("utf-8")
           
           date = json.loads(html)
           ev_type = date[0]['type']
           
           # We only count commits and repo creation events, as they do also contain commits
           if ev_type != "PushEvent" and ev_type != "CreateEvent":
               raise DoesNotCount()

           date = date[0]["created_at"]
           return date

# Check if a commit has been made yesterday. If it has, congratulate. If not, swear.
def has_committed(user):
    try:
        commit_date = get_last_commit_date(user)
        yesterday = int(time.strftime("%d")) - 1 
        yesterdate = time.strftime("%Y-%m-") + str(yesterday)

        if commit_date[:10] == yesterdate:
            return True
    except DoesNotCount:
        pass

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

# If the user has not committed, send an email to the recipient
def check(user):
    if not has_committed(user):
        mail(user)

# This must be run with the username of the user to be checked as an argument
if __name__ == "__main__":
    for user in USER:
    	check(user)

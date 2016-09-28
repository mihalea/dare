#!/usr/bin/env python3

import urllib.request
import sys
import time
import json

# Get the last commit's date for $user as a string formatted as follows: %Y-%m-%dT%HH:%mm:%ssZ
def get_last_commit_date(user):
    with urllib.request.urlopen('https://api.github.com/users/' + user + '/events') as response:
           html = response.read().decode("utf-8")
           date = json.loads(html)
           date = date[0]["created_at"]
           return date

# Check if a commit has been made yesterday. If it has, congratulate. If not, swear.
def check(user):
    commit_date = get_last_commit_date(user)
    yesterday = int(time.strftime("%d")) - 1
    yesterdate = time.strftime("%Y-%m-") + str(yesterday)

    if commit_date[:10] != yesterdate:
        print("Cheeky bastard!")
    else:
        print("Well, good job!")

# This must be run with the username of the user to be checked as an argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide a username as the only argument")
    else:
        check(sys.argv[1])

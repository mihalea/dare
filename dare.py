#!/usr/bin/env python3

import urllib.request
import sys
import time
import json

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

# This must be run with the username of the user to be checked as an argument
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide a username as the only argument")
    else:
        print(has_committed(sys.argv[1]))

#!/usr/bin/env python3

import urllib.request
import sys


def get_last_commit_date(user):
    with urllib.request.urlopen('http://python.org/') as response:
           html = response.read()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide a username as the only parameter")
    else:
        print("Yay")

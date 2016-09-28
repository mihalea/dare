# dare

Monitor your friends with this simple python script so that you know when they skip a day of programming. To get this up and running you just need a local mail server running on your machine. Once you get that ticked you should edit `config.py` and make it yours.

This can be easily be run daily with logs using cron. To have it run every morning at 10 you would have `0 10 * * * python3 /opt/dare/dare.py >> /opt/dare/dare.log`.

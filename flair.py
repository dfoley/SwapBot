import re
import json
import praw
import time
import datetime
import os.path

debug = False

# Gets the absolute path to the directory in which the script exists, then adds a trailing /
fdir = os.path.abspath(os.path.dirname(__file__)) + '/'

f = open(fdir + "config.txt", "r")
info = f.read().splitlines()
f.close()

subreddit_name = info[0]
client_id = info[1]
client_secret = info[2]
bot_username = info[3]
bot_password = info[4]

fc = open(fdir + "flairconfig.txt", "r")
flairtemp = fc.read().splitlines()
fc.close()

def update_flair(sub):
    flairs = sub.flair(limit=None)
    # Loop over each author and change their flair
    for flair in flairs:
        css = flair['flair_text']
        css = css.strip(' Swaps')   #Strips ' Swaps' from the string leaving only a number
        if 0 <= int(css) < 5:
            template = flairtemp[0]
        elif 5 <= int(css) < 10:
            template = flairtemp[1]
        elif 10 <= int(css) < 20:
            template = flairtemp[2]
        elif 20 <= int(css) < 30:
            template = flairtemp[3]
        elif 30 <= int(css) < 40:
            template = flairtemp[4]
        elif 40 <= int(css) < 50:
            template = flairtemp[5]
        elif 50 <= int(css) < 60:
            template = flairtemp[6]
        elif 60 <= int(css) < 70:
            template = flairtemp[7]
        elif 70 <= int(css) < 80:
            template = flairtemp[8]
        elif 80 <= int(css) < 90:
            template = flairtemp[9]
        elif 90 <= int(css) < 100:
            template = flairtemp[10]
        elif 100 <= int(css) < 200:
            template = flairtemp[11]
        elif 200 <= int(css) < 300:
            template = flairtemp[12]
        elif 300 <= int(css) < 400:
            template = flairtemp[13]
        elif 400 <= int(css) < 500:
            template = flairtemp[14]
        elif 500 <= int(css) < 600:
            template = flairtemp[15]
        elif 600 <= int(css) < 700:
            template = flairtemp[16]
        elif 700 <= int(css) < 800:
            template = flairtemp[17]
        elif 800 <= int(css) < 900:
            template = flairtemp[18]
        elif 900 <= int(css):
            template = flairtemp[19]
        else:
            print("Invalid data: " + css)
            continue

        print(str(flair['user']) + " - " + css + " Swaps")
        sub.flair.set(str(flair['user']).lower(), css+" Swaps", flair_template_id=template)

    print("Updating Reddit now...")

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent='UserAgent', username=bot_username, password=bot_password)
sub = reddit.subreddit(subreddit_name)
update_flair(sub)

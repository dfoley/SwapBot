## Features

* Users can tag the name of the bot and the name of the person they traded with in their trade thread to invoke the bot. When the tagged user replies to the comment with "confirmed" the bot will reply with "Swap has been confirmed!" and give them credit.

* Users can send a message to the bot with u/<some_username> in the body of the message to get the feedback score for that person.

## Basic Run Instructions

* Clone this repository using `git clone`

* Create a `config.txt` file with these five attributes, in this order, each on their own line (the .gitignore will prevent you from uploading this file to the repo):

   * The name of the subreddit you want to run on e.g. `steelbookswap`

   * Reddit API client ID

   * Reddit API client secret

   * Reddit Bot Username

   * Reddit Bot Password

* Delete the Forked database files by entering:
    
   * rm database/*

* Using the subreddit name from above (case matters), create the following data files in the **~/SwapBot/database** directory:

   * `swaps-<YOUR_SUBREDDIT_NAME>.json`

   * `active_comments-<YOUR_SUBREDDIT_NAME>.txt`


* Add the following cronjob using `crontab -e` 

    * `*/2 * * * * cd ~/<YOUR_DIRECTORY_NAME> && python swap.py;`
    
## Using Git to back up the Database Files

Because this script uses json files to store the data, it can be useful to have a backup of the data somewhere. Git is convenient for this. By creating your own github repository, you can push your data files to the remote server once an hour to ensure proper back up and be able to recover should anything go wrong. Follow these steps to do so:

* Create your own directory for your version of the script and move all visible files (files that do not start with a `.`) and the .gitignore to the new directory.

* Initialize the directory as a new git repository (this assumes you are already signed in to git on your machine).

* Add the following cronjob to your server with `crontab -e` to enable creating hourly backups of the data files:

    * `0 * * * * cd ~/<YOUR_DIRECTORY_NAME> && git pull; git add *; git commit -am "Hourly Upload"; git push;`

## Legacy Trades

The code references Legacy Trades. These are confirmed trades from before you bring the bot online. 
It recognizes a legacy trade only if it appears in the database file. 
If you have no record of trades before bringing this bot online, you can ignore legacy trades. 
If you wish to give credit to your users from their legacy trades, you will have to write your own script to do so. 
The general idea is to write entries in the json file for username: ["LEGACY TRADE", "LEGACY TRADE"] for as many legacy trades as that person had. 
Once you have the backfilled json file in the database folder, the script will use those legacy trades when showcasing the user reputation

## Flair - Old and New

I have created a template old.reddit.css file that has the css code you want to add into your stylesheet. I have them broken into tiers, 0-4, 5-9, 10-19, 20-29, etc, then once it surpasses 99 they are grouped by the hundred (100-199, 200-299, etc) all the way up to 999. I already have all colors picked out, but feel free to change them to fit your sub. 

* Copy the old.reddit.css stylesheet into your old.reddit stylesheet.

* Create the user flairs by going to the redesign Mod Tools > Community appearance > User flair. The flair text should match with the css code. ex: 0-4, 5-9, 10-19, etc.

    * Add the hex background-color from the css code that corresponds to the flair, and choose light or dark text.
    
    * After you create each flair, open it back up for editing and click Copy ID at the top to copy the flair_template_id. Paste this code into what will be your `flairconfig.txt` file, one id per line.

* Once you have created them, the flairs should appear on the old.reddit as well, but without any colors. Go to your old.reddit > Edit Flair > User Flair Templates. Add the corresponding CSS Class to each flair. The colors should start to appear since you have already setup the stylesheet.

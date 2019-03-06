

## Prerequisites
This setup assumes you already have or know a few things:

 1. [Format and Write Raspbian to a microSD card](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) as well as basic terminal usage
 2. [GitHub account](https://github.com/)
 3. Fork from the [Original Repo](https://github.com/funkopopmod/SwapBot)
 4. Dedicated [Reddit account](https://www.reddit.com/register/) for your SwapBot
 5. [Reddit Application](https://www.reddit.com/prefs/apps) for the Reddit API client ID and client secret

## Initial Setup
Image your microSD Card with the most recent version of [Raspbian](https://www.raspberrypi.org/downloads/raspbian/).

I'm going to walk you through a headless setup, which requires **WiFi**, enabling **ssh**, and then you can enable **VNC** to remote in to access the desktop. If you plan to connect your device to a monitor and keyboard to do gui setup, you can skip down to the last part of this section before the Git Section.

In the **/boot** directory, create the following files:

* `ssh`
* `wpa_supplicant.conf`
    
The `ssh` file is empty and has no file extension. The contents of `wpa_supplicant.conf` should look like this:

    country=US
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
        ssid="your_real_wifi_ssid"
        scan_ssid=1
        psk="your_real_password"
        key_mgmt=WPA-PSK
    }

Power up Pi and let it run for a few minutes until the status LED stops blinking.

Your device should be reachable at **raspberrypi.local** If not, find your device's IP address. There are many ways to do this, hopefully you know how to for your network.

Connect to your device through your preferred SSH Client (Windows: [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), Macs can use Terminal with the **ssh pi@raspberrypi.local** command. You should be prompted to login. The default login is:

*   **username:** pi
*   **password:** raspberry

You may be prompted to change your password since ssh is enabled. You can do this now or when you **VNC** to the desktop as the **Setup wizard** will be on the screen. Save this password for your records.

Now that you're connected, we're going to enable **VNC** by doing the following:
    
    sudo raspi-config

*   Navigate to  **Interfacing Options**.
    
*   Scroll down and select  **VNC** then enter **Yes**.

You can now VNC into your Pi for the desktop experience and launch Terminal to continue, but you can also continue most of this via your SSH Client.

* From Terminal/SSH Client, execute the following commands:
   
       sudo apt-get update
       sudo apt-get upgrade
   
   *When prompted about upgrading packages, enter **y**. Let the packages upgrade, this may take a while.*
 * From the Desktop run through the Setup wizard, mainly allowing it to check for updates.

**Last before we move on, you want to execute the following command:**

    sudo pip install praw

## Git Setup
At this point you should have your GitHub account setup with it's own Fork from the [FunkoPopMod Repo](https://github.com/funkopopmod/SwapBot).

git should already be installed from running the updates, but just in case:

    sudo apt install git

Now you need to configure git with your account info

    sudo git config --system user.name "GitHubUsername"
    sudo git config --system user.email "YourGitHub@Email.com"
    sudo git config --system core.editor nano

Next you're going to clone your Forked Repo to your pi. This should install at **/home/\<user>/SwapBot** (default user is pi)

    git clone https://github.com/<YOUR_REPO>/SwapBot.git
    cd ~/SwapBot
    git init 

You should get a message saying it's reinitialized an existing git repository.

Create a `config.txt` file with these five attributes, in this order, each on their own line (the .gitignore will prevent you from uploading this file to the repo):

   * The name of the subreddit you want to run on e.g. `steelbookswap`

   * Reddit API client ID

   * Reddit API client secret

   * Reddit Bot Username

   * Reddit Bot Password

Delete the Forked database files by entering:
    
    rm database/*

Using the subreddit name from above (case matters), create the following data files in the **~/SwapBot/database** directory:

* `swaps-<YOUR_SUBREDDIT_NAME>.json`

* `active_comments-<YOUR_SUBREDDIT_NAME>.txt`

Once that's finished, run the following commands:

    git add --all
    git status
    git commit -am "Description of Update"
    git remote add origin git@github.com:GitHubUsername/SwapBot.git
    git push -u origin master

Enter your GitHub username and password if asked.

This should successfully push any changes you've made (such as the /database files) to your GitHub repo.

## SSH-Keys Setup 
*I couldn't get this part working properly; git pull, add, and commit all worked, but push wouldn't. If you cannot get them working, skip down to the* SwapBot/.git/config Section *below. But these are the instructions as I understand them.*

Now we're going to generate SSH-Keys for your GitHub account.

First, check for existing SSH Keys:

    ls -al ~/.ssh

At this point it should return nothing.

Generate a new SSH-Key:

    ssh-keygen -t rsa -b 4096 -C "YourGitHub@Email.com"

Wait for Keys to be generated. Once it finishes, press enter to assume the filename `id_rsa`

Enter a passphrase, then enter it again. Save this passphrase for your records.

Check if SSH-Agent is running

    eval $(ssh-agent -s)
    
This should output **Agent pid #####**

Add your SSH private key to the ssh-agent

    ssh-add ~/.ssh/id_rsa

Copy contents of **id_rsa.pub** to your clipboard

Navigate to **GitHub > Settings > SSH and GPG Keys** and click [**New SSH Key**](https://github.com/settings/ssh/new).

Enter a Title, then paste your clipboard in the large textarea.

Click **Add SSH Key** to finish up with GitHub.

## Optional - SwapBot/.git/config
Only needed if you cannot get the SSH-Key above to work properly. This manually puts your **GitHubUsername** and **GitHubPassword** into the `config` file.

Navigate to **~/SwapBot/.git** and open the `config` file in Text Editor. You're going to change the **url** variable from:

	url = https://github.com/<GitHubUsername>/SwapBot.git

To: 

	url = https://<GitHubUsername>:<GitHubPassword>@github.com/<GitHubUsername>/SwapBot.git

At this point you should have no problems with the crontab jobs in the next section.

## crontab Jobs
This creates a task to run the script at a schedule time. In the beginning it's good to setup logging to see if something is going wrong. To do this, add **>> /tmp/filename.txt 2>&1** before the **;** at the end of each command. When you've got everything working, you can remove it and just leave the ending **;**.

    crontab -e

If prompted, choose **nano** and press enter. Scroll down to the bottom of the file and enter

    */2 * * * * cd ~/SwapBot && python swap.py>> /tmp/swap.txt 2>&1;

Press **Ctrl+X**,  enter **Y**  to save changes, and press **Enter** once more to confirm.

Next is to schedule git to update your repo once an hour. To get proper permissions, you're going to use **sudo** this time.

    sudo crontab -e
    
If prompted, choose **nano** and press enter. Scroll down to the bottom of the file and enter

    0 * * * * cd /home/<user>/SwapBot && git pull; git add *; git commit -am "Hourly Upload"; git push;

Press **Ctrl+X**,  enter **Y**  to save changes, and press **Enter** once more to confirm.

At this point everything should be working. You can test it out by changing the **0** at the beginning of the git cronjob with ***/2** to have it run once every 2 minutes instead of at the beginning of every hour. You can then try to make a change locally on your Pi and watch for the push update on your GitHub repo. Then make a change on your repo, and watch on your Pi for it to pull the changes. Once you have this figured out, don't forget to change it back to 0 so it is only backing up once an hour.

## Optional - Scheduled Reboot
You can add a job to reboot the Pi at a specified time. I chose 11:59pm because it should be able to get back up in time for the midnight run of the `swap.py` cronjob. I do this to make sure the system doesn't run for too long without a refresh. 

    sudo crontab -e
    
Scroll down to the bottom of the file and enter

    59 23 * * * reboot;

Press **Ctrl+X**,  enter **Y**  to save changes, and press **Enter** once more to confirm.

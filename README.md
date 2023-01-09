# GithubTracker

**(Still under construction)**<br>

After finishing the ironhack data-analytics bootcamp I wanted to keep track of the<br>
other students repositories to see if one starts a new interesting project.<br>
But I'm too lazy to do this manually by surfing through all these github accounts,<br>
so I made some experiments in web scraping and html parsing and this is what happend...<br>


## Description

A python written tool for scraping accounts from github.com, to see if someone created a new<br>
repository or ther're recent commits. It comes with a simple-to-use graphical user interface.
<pre>
Usage: python main.py [OPTIONS ...]

-h, --help            Show this helptext and exit
-d, --basedir=PATH    Set alternate base directory
</pre>


## Run

<pre>
$ cd github_tracker/src/
$ python main.py
</pre>


## Storage

Since account names and images are stored, a small directory tree is required to exist.<br>
Running github-tracker the first time, that directory tree will be created.
<pre>
~/.github_tracker             
   |__ accounts.txt      Textfile holding the account names
   |__ avatars/          Directory for account avatar images
       |__ account.jpg
       |__ account.jpg
       |__ ...
</pre>


## Screenshots

<p style="clear:left;">
    The main view shows all github accounts currently handled by github-tracker.<br>
    Here you can add new accounts or delete existing ones.<br>
    Clicking on the menu item View, different methods can be selected to sort accounts.
</p>
<img width='500' style="float:left;" src='https://raw.githubusercontent.com/lukwies/github_tracker/main/screenshots/screenshot_1.png'>

<p style="clear:left;">
    <br><br>
    After selecting an account on the previous view, you'll endup at the account view.<br>
    Here you can see more details about the github account owner and all its repositories.<br>
    The repositories can be sorted by last commit date or repo name.<br>
    Clicking on some of the labels will open any github urls in the default browser.
</p>
<img width='500' style="clear:both; float:left" src='https://raw.githubusercontent.com/lukwies/github_tracker/main/screenshots/screenshot_2.png'>

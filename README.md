# GithubTracker

After finishing the ironhack data-analytics bootcamp I wanted to keep track of the<br>
other students repositories to see if one starts a new interesting project.<br>
But I'm too lazy to do this manually by surfing through all these github accounts,<br>
so I made some experiments in web scraping and html parsing and this is what happend...<br>


## Description

github-tracker is a python written tool for scraping account informations from github.com.<br>
It comes with a nice and simple Tkinter graphical user interface [Screenshots](#Screenshots).<br>


## Start Program

<pre>
$ cd github_tracker/
$ python main.py
</pre>


## Config directory

Since account names and images are stored, a small directory tree is required to exist.<br>
Running github-tracker the first time, that dirtree will be created.
<pre>
~/.github_tracker             
   |__ accounts.txt      Textfile holding the account names
   |__ avatars/          Directory for account avatar images
       |__ user1.jpg
       |__ user2.jpg
       |__ ...
</pre>


## Screenshots

<img width='400' style="float:left;" src='https://raw.githubusercontent.com/lukwies/github_tracker/main/screenshots/screenshot_1.png'>
<p style="clear:left;"><br>
    The main view shows all github accounts currently handled by the github-tracker.<br>
    Here you can add new accounts or delete existing ones.<br>
    Clicking on the menu item View, different methods can be selected to sort accounts.
</p>
<br><br>
<img width='400' style="clear:both; float:left" src='https://raw.githubusercontent.com/lukwies/github_tracker/main/screenshots/screenshot_2.png'>
<p style="clear:left;"><br>
    After selecting an account on the previous view, you'll endup at the account view.<br>
    Here you can see more details about the github account owner and all its repositories.<br>
    The repositories can be sorted by last commit date or repo name.<br>
    Clicking on some of the labels will open any github urls in the default browser.
</p>

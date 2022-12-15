# GithubTracker

After finishing the ironhack data-analytics bootcamp I wanted to keep track of
the other students repositories to see if one starts a new interesting project.
But I'm too lazy to do this manually by surfing through all this github accounts,
so I made some experiments in web scraping and html parsing and this is what happend...


## Usage

	`python main.py`

## Install

For installing the github tracker there's a simple bash script.<br>
Running that script under linux or mac:
	`./install.sh`


### Config directory

The github tracker needs a config directory to store:
- Names of accounts added by the user
- Avatar images
- Icons (coming up)

<pre>
	~/.github_tracker
	   |__ accounts.txt
	   |__ avatars/
	   |   |__ user1.jpg
	   |   |__ user2.jpg
	   |   |__ ...
	   |__ res/
               |__ ...
</pre>


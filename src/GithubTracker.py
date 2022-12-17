import logging
from os.path import expanduser
import os
import sys

from View import *
from GithubAccount import *
from util import *

BASEDIR  = '.github_tracker'
LOGLEVEL = logging.INFO
LOGFMT   = '%(levelname)s  %(message)s'


class GithubTracker:

	def __init__(self):
		logging.basicConfig(level=LOGLEVEL, format=LOGFMT)
		self.basedir   = os.path.join(expanduser("~"), BASEDIR)
		self.avatardir = os.path.join(self.basedir, "avatars")
		self.namefile  = os.path.join(self.basedir, "accounts.txt")
		self.account_names = []	# List with account names read from accounts.txt
		self.accounts = []	# List with GithubAccount instances
		self.view     = None


	def run(self, basedir=None):
		if self.prepare(basedir):
			self.view = View(self)
			self.view.run()

	def status_msg(self, text, clear_after=0):
		if self.view != None:
			self.view.msg(text, clear_after)
		logging.info(text)


	def prepare(self, basedir=None):
		'''
		This makes sure everything is setup before starting the gui.
		1) Check if config dir exists, if not -> create it
		2) Check if we're connected to the internet and github.com is up
		3) Load account names from basedir/accounts.txt

		Args:
			basedir: Path to config basedir (Default: ~/.github_tracker).
		Return:
			True on success, False on error
		'''
		if basedir:
			self.basedir   = basedir
			self.avatardir = os.path.join(self.basedir, "avatars")
			self.namefile  = os.path.join(self.basedir, "accounts.txt")

		# Create config directory if not exist
		if not os.path.isdir(self.basedir):
			try:
				logging.info("Creating config directory at '{self.basedir}'")
				os.mkdir(self.basedir)
				os.mkdir(self.avatardir)
			except:
				logging.error(f"Failed to create config directory '{self.basedir}'")
				return False

		# Check if we can reach the internet and github.com is up and running.
		if not internet_is_reachable():
			logging.error("Not connected to the internet!")
			return False
		elif not page_is_reachable('https://github.com'):
			logging.error("Host https://github.com seems to be down :-(")
			logging.error("Please check this manually!")
			return False

		# Read account names from file 'accounts.txt' if exists.
		self.account_names = []
		if os.path.isfile(self.namefile):
			with open(self.namefile, 'r') as file:
				lines = file.readlines()

			for line in lines:
				line = line.strip()
				if len(line) > 0 and line[0] != '#':
					self.account_names.append(line)
		logging.info("Read {} account names from {}"
				.format(len(self.account_names),
					self.namefile))
		return True

	def is_account(self, account_name):
		'''
		Return True if account with given name exists.
		'''
		for a in self.accounts:
			if account_name == a.username:
				return True
		return False


	def sort_accounts(self, by='commit', reverse=False):
		if by == 'commit':
			self.accounts.sort(key=lambda x: x.last_commit, reverse=reverse)
		elif by == 'repos':
			self.accounts.sort(key=lambda x: len(x.repos), reverse=reverse)
		elif by == 'name':
			self.accounts.sort(key=lambda x: x.username.casefold(), reverse=reverse)

		self.view.open_account_list_view()


	def store_accounts(self):
		'''
		Store account names to basedir/accounts.txt
		'''
		with open(self.namefile, 'w') as file:
			[ file.write(a.username + '\n') for a in self.accounts ]


	def delete_account(self, account):
		'''
		Delete given account from the account list. To delete the account
		permanently overwrite the accounts.txt file (basedir/accounts.txt).
		'''
		self.accounts.remove(account)
		self.store_accounts()


import logging
from os.path import expanduser
import os
import sys

from View import *
from GithubAccount import *

BASEDIR  = '.github_tracker'
LOGLEVEL = logging.INFO
LOGFMT   = '%(levelname)s  %(message)s'


class GithubTracker:

	def __init__(self):
		logging.basicConfig(level=LOGLEVEL, format=LOGFMT)
		self.basedir = os.path.join(expanduser("~"), BASEDIR)
		self.account_names = []	# List with account names read from accounts.txt
		self.accounts = []	# List with GithubAccount instances
		self.view = None


	def run(self, config_path=None):
		self.load_configs(config_path)

		# Scrape all github accounts we have a name for
		for aname in self.account_names:
			acc = GithubAccount(aname)
			if acc.download(os.path.join(self.basedir, "avatars")):
				self.accounts.append(acc)

		# Sort accounts by last commit
#		self.accounts.sort(key=lambda x: x.

		self.view = View(self)
		self.view.run()

	def status_msg(self, text, clear_after=0):
		if self.view != None:
			self.view.msg(text, clear_after)
		logging.info(text)


	def load_configs(self, config_path=None):
		'''
		After making sure that the config tree exists, read account names
		from configdir/accounts.txt.
		If no config path is given, the default is used (~/.github_tracker).

		Args:
			config_path: Alternate config path
		'''

		if config_path:
			self.basedir = config_path

		# Create config directory if not exist
		if not os.path.isdir(self.basedir):
			try:
				logging.info("Creating config directory at '{self.basedir}'")
				os.mkdir(self.basedir)
				os.mkdir(os.path.join(self.basedir, "avatars"))
			except:
				logging.error(f"Failed to create config directory '{self.basedir}'")
				sys.exit(1)


		# Read account names from file 'accounts.txt' if exists.
		accounts_file = os.path.join(self.basedir, "accounts.txt")
		self.account_names = []

		if os.path.isfile(accounts_file):
			with open(accounts_file, 'r') as file:
				lines = file.readlines()

			for line in lines:
				line = line.strip()
				if len(line) > 0 and line[0] != '#':
					self.account_names.append(line)

	def store_account_names(self):
		'''
		Store account names to ~/.github_tracker/accounts.txt
		'''
		p = os.path.join(self.basedir, 'accounts.txt')
		with open(p, 'w') as file:
			[ file.write(name + '\n') for name in self.account_names ]


	def add_account(self, account_name):
		'''
		Download github account info for given account name and
		add it to the account list. To store the account permanently
		write all account names to a text file (basedir/accounts.txt)
		'''

		if account_name in self.account_names:
			self.status_msg(f"Account '{account_name}' already exists", 3)
			return False

		account = GithubAccount(account_name)
		self.status_msg(f"Downloading account '{account_name}' ...", 4)

		if account.download(os.path.join(self.basedir, 'avatars')):
			self.account_names.append(account_name)
			self.accounts.append(account)
			self.store_account_names()
			return True

		return False


	def delete_account(self, account):
		'''
		Delete given account from the account list. To delete the account
		permanently overwrite the accounts.txt file (basedir/accounts.txt).
		'''
		self.account_names.remove(account.username)
		self.accounts.remove(account)
		self.store_account_names()

	def sort_accounts(self, by='commit', ascending=True):
		if by == 'commit':
			self.accounts.sort(key=lambda x: x.last_commit, reverse=ascending)
			self.status_msg('Sorted by date of last commit', 3)
		elif by == 'repos':
			self.accounts.sort(key=lambda x: len(x.repos), reverse=ascending)
			self.status_msg('Sorted by number of repositories', 3)
		elif by == 'name':
			self.accounts.sort(key=lambda x: x.username, reverse=ascending)
			self.status_msg('Sorted by name of account', 3)

		self.view.open_account_list_view()


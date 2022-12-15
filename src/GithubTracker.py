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
		self.basedir = expanduser("~") + '/' + BASEDIR
		self.account_names = []	# List with account names read from accounts.txt
		self.accounts = []	# List with GithubAccount instances
		self.view = None


	def run(self, config_path=None):
		self.load_configs(config_path)

		# Scrape all github accounts we have a name for
		for aname in self.account_names:
			acc = GithubAccount(aname)
			if acc.download(self.basedir + "/avatars"):
				self.accounts.append(acc)

		# Sort accounts by last commit
#		self.accounts.sort(key=lambda x: x.

		self.view = View(self)
		self.view.run()

	def status_msg(self, text, clear_after=0):
		if self.view != None:
			self.view.statusbar.msg(text, clear_after)
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
				os.mkdir(self.basedir + "/avatars")
			except:
				logging.error(f"Failed to create config directory '{self.basedir}'")
				sys.exit(1)


		# Read account names from file 'accounts.txt' if exists.
		accounts_file = self.basedir + "/accounts.txt"
		account_names = []

		if os.path.isfile(accounts_file):
			with open(accounts_file, 'r') as file:
				lines = file.readlines()

			for line in lines:
				if line[0] != '#':
					self.account_names.append(line.strip())

	def store_account_names(self):
		'''
		Store account names to ~/.github_tracker/accounts.txt
		'''
		p = os.path.join(self.basedir, 'accounts.txt')
		with open(p, 'w') as file:
			[ f.write(name + '\n') for name in self.account_names ]

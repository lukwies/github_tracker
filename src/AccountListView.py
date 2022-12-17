import tkinter as tk
from AccountListFrame import *
from GithubAccount import *

from widgets import LeftLabel

class AccountListView(tk.Frame):

	def __init__(self, parent, tracker, view):
		'''
		Account list view.

		Args:
			parent:  Parent tkinter widget
			tracker: GithubTracker instance
		'''
		super().__init__(parent)

		self.tracker = tracker
		self.view = view
		self.frNoAcc = None
		self.max_row = 0
		self.setup()

	def add(self, account):
		'''
		Add account to List View.
		'''

		# Remove label showing that there are no accounts available
		if self.frNoAcc:
			self.frNoAcc.destroy()

		AccountListFrame(self, account, self.tracker).grid(
				row=self.max_row, column=0, sticky='nswe')
		self.max_row += 1

	def setup(self):
                # Setup menu
		self.view.menu.entryconfig('Account', state='normal')
		self.view.menuView.entryconfig('Sort by last commit', state='normal',
			command=lambda: self.tracker.sort_accounts('commit', True))
		self.view.menuView.entryconfig('Sort by name', state='normal',
			command=lambda: self.tracker.sort_accounts('name', False))
		self.view.menuView.entryconfig('Sort by number of repos', state='normal',
			command=lambda: self.tracker.sort_accounts('repos', True))

		self.grid_columnconfigure(0, weight=1)

		if len(self.tracker.accounts) > 0:
			# We have acctounts
			for acc in self.tracker.accounts:
				AccountListFrame(self, acc, self.tracker).grid(
						row=self.max_row, column=0, sticky='nswe')
				self.max_row += 1
		else:
			# No accounts, show NoAccountsFrame
			self.frNoAcc = NoAccountsFrame(self, self.tracker)
			self.frNoAcc.grid(row=0, column=0, sticky='nswe')


class NoAccountsFrame(tk.Frame):
	'''
	Frame showing up if no github accounts are available.
	'''
	def __init__(self, parent, tracker):
		super().__init__(parent)
		self.tracker = tracker

		self.hdr = LeftLabel(self, text='No accounts available!',
				font='Arial 12 bold')
		self.text = LeftLabel(self, font='Arial 9')
		self.setup()

	def setup(self):
		self.grid_columnconfigure(0, weight=1)

		txt =   "You can add an account either going to menu item Accounts->Add\n"\
			"and enter any github user name or adding one or more account names\n"\
			"to the file '{}'.\n".format(self.tracker.namefile)
		self.text.configure(text=txt)

		self.hdr.grid(row=0, column=0, sticky='nswe')
		self.text.grid(row=1, column=0, sticky='nswe', pady=5)

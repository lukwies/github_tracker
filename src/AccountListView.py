import tkinter as tk
from AccountListFrame import *
from GithubAccount import *


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
		self.max_row = 0
		self.setup()

	def add(self, account):
		'''
		Add account to List View.
		'''
		AccountListFrame(self, account, self.tracker).grid(
				row=self.max_row, column=0, sticky='nswe')
		self.max_row += 1

	def setup(self):
                # Setup menu
		self.view.menu.entryconfig('Account', state='normal')
		self.view.menuView.entryconfig('Sort by last commit', state='normal',
			command=lambda: self.tracker.sort_accounts('commit'))
		self.view.menuView.entryconfig('Sort by name', state='normal',
			command=lambda: self.tracker.sort_accounts('name', False))
		self.view.menuView.entryconfig('Sort by number of repos', state='normal',
			command=lambda: self.tracker.sort_accounts('repos'))

		self.grid_columnconfigure(0, weight=1)

		for acc in self.tracker.accounts:
			AccountListFrame(self, acc, self.tracker).grid(
					row=self.max_row, column=0, sticky='nswe')
			self.max_row += 1


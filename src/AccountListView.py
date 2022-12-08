import tkinter as tk
from AccountListFrame import *



class AccountListView(tk.Frame):

	def __init__(self, parent, tracker):
		'''
		Account list view.

		Args:
			tracker: GithubTracker instance
		'''
		super().__init__(parent)

		self.tracker = tracker
		self.__setup()


	def __setup(self):

		self.grid_columnconfigure(0, weight=1)

		y=0
		for account in self.tracker.accounts:
			AccountListFrame(self, account, self.tracker).grid(
				row=y, column=0, sticky='nswe')
			y += 1

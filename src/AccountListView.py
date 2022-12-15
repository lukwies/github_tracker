import tkinter as tk
from AccountListFrame import *
from GithubAccount import *


class AccountListView(tk.Frame):

	def __init__(self, parent, tracker):
		'''
		Account list view.

		Args:
			parent:  Parent tkinter widget
			tracker: GithubTracker instance
		'''
		super().__init__(parent)

		self.tracker = tracker
		self.__setup()


	def __setup(self):

		self.grid_columnconfigure(0, weight=1)

		for i, acc in enumerate(self.tracker.accounts):
			AccountListFrame(self, acc, self.tracker).grid(
					row=i, column=0, sticky='nswe')


import tkinter as tk
import logging

from AccountView import *
from AccountListView import *

class View:
	def __init__(self, tracker):
		'''
		Main view.

		Args:
			tracker: GithubTracker instance
		'''
		self.tracker = tracker
		self.root = tk.Tk()
		self.root.title('github tracker')

		self.menu = tk.Menu(self.root)
		self.root.configure(menu=self.menu)
		self.menuFile    = tk.Menu(self.menu)
		self.menuAccount = tk.Menu(self.menu)

		self.statusbar = tk.Frame(self.root) #StatusBar(self.root)
		self.mainframe = AccountListView(self.root, tracker)
		self.mainframe.grid(row=0, column=0, sticky='nswe')

		self._setup()


	def run(self):
		self.root.mainloop()


	def open_account_list_view(self):
		self.mainframe.destroy()
		self.mainframe = AccountListView(self.root, tracker)
		self.mainframe.grid(row=0, column=0, sticky='nswe')

	def open_account_view(self, account):
		self.mainframe.destroy()
		logging.info(f"Open account '{account.username}'")
		self.mainframe = AccountView(self.root, account, self.tracker)
		self.mainframe.grid(row=0, column=0, sticky='nswe')

	def msg(self, text, clear_after=0):
		self.msglbl = LeftLabel(self.statusbar, text=text, font='Arial 10',
				fg='grey', bg='#303030')
		self.msglbl.grid(row=0, column=0, sticky='nw')

		if clear_after > 0:
			self.msglbl.after(clear_after*1000, self.clear)

	def clearmsg(self):
		self.msglbl.destroy()


	def _setup(self):
		self.menu.configure(background='#303030', foreground='#fefefe')
		self.menu.add_cascade(label='File', menu=self.menuFile)
		self.menu.add_cascade(label='Account', menu=self.menuAccount)
		self.menuFile.add_command(label="Exit", command=self.root.destroy)
		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_rowconfigure(0, weight=1)

		self.statusbar.configure(bg='#303030', height=30,
			highlightbackground="#454545", highlightthickness=1)
		self.statusbar.grid(row=1, column=0, sticky='nswe')
		#self.statusbar.msg('Hello World', 3)



class StatusBar(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)




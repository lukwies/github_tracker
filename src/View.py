import tkinter as tk
from tkinter import simpledialog
import logging

from AccountView import *
from AccountListView import *
from widgets import *

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
		self.root.geometry('640x400')

		self.menu = tk.Menu(self.root)
		self.root.configure(menu=self.menu)
		self.menuFile    = tk.Menu(self.menu)
		self.menuAccount = tk.Menu(self.menu)
		self.menuView    = tk.Menu(self.menu)

		self.mainframe = AccountListView(self.root, tracker)
		self.mainframe.grid(row=0, column=0, sticky='nswe')
		self.msgframe = None
#		self.statusbar = tk.Frame(self.root) #StatusBar(self.root)

		self._setup()
#		self.msg('Hello World', 4)


	def run(self):
		self.root.mainloop()


	def open_account_list_view(self):
		self.mainframe.destroy()
		self.mainframe = AccountListView(self.root, self.tracker)
		self.mainframe.grid(row=0, column=0, sticky='nswe')

	def open_account_view(self, account):
		self.mainframe.destroy()
		logging.info(f"Open account '{account.username}'")
		self.mainframe = AccountView(self.root, account, self.tracker)
		self.mainframe.grid(row=0, column=0, sticky='nswe')

	def msg(self, text, clear_after=0, fg='#f8f8f8'):
		self.msglbl = LeftLabel(self.root, text=' '+text, font='Arial 11',
				fg=fg, bg='#303030')
		self.msglbl.grid(row=1, column=0, sticky='nswe')
		if clear_after > 0:
			self.msglbl.after(clear_after*1000, self.clearmsg)

	def clearmsg(self):
		self.msglbl.destroy()


	def _setup(self):
		self.menu.configure(background='#303030', foreground='#fefefe')
		self.menu.add_cascade(label='File', menu=self.menuFile)
		self.menu.add_cascade(label='Account', menu=self.menuAccount)
		self.menu.add_cascade(label='View', menu=self.menuView)
		self.menuFile.add_command(label="Exit", command=self.root.destroy)
		self.menuAccount.add_command(label="Add", command=self._add_account)
		self.menuView.add_command(label="Sort by last commit",
				command=lambda: self.tracker.sort_accounts('commit'))
		self.menuView.add_command(label="Sort by name",
				command=lambda: self.tracker.sort_accounts('name', False))
		self.menuView.add_command(label="Sort by number of repos",
				command=lambda: self.tracker.sort_accounts('repos'))

		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_rowconfigure(0, weight=1)

#		self.statusbar.configure(bg='#303030', height=30,
#			highlightbackground="#454545", highlightthickness=1)
#		self.statusbar.grid(row=2, column=0, sticky='nswe')
		self.msg(f'Loaded {len(self.tracker.accounts)} github accounts', 3)


	def _add_account(self):
		'''
		Callback for menu item 'Account->Add'
		'''
		acc_name = simpledialog.askstring(parent=self.root, title='Add account',
				prompt='Account Name:')
		if acc_name:
			self.tracker.add_account(acc_name)
			self.open_account_list_view()



class MsgFrame(tk.Frame):
	def __init__(self, parent, text, is_error, clear_after=0):
		super().__init__(parent, height=30, bg='#454545')

		self.lbl = LeftLabel(self, text=text, fg='#f00000' if is_error else 'white')
		self.lbl.grid(row=0, column=0, sticky='nw')

		if clear_after > 0:
			self.after(clear_after*1000, self.destroy)

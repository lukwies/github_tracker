import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import logging
from threading import Thread
import time

from AccountView import *
from AccountListView import *
from AvatarView import *
from widgets import *


class View:
	'''
	Main View.
	'''
	def __init__(self, tracker):
		'''
		Args:
			tracker: GithubTracker instance
		'''
		self.tracker = tracker
		self.root = tk.Tk()
		self.root.title('github tracker')
		self.root.geometry('640x400')

		self.menu = tk.Menu(self.root)
		self.root.configure(menu=self.menu)
		self.menuFile    = tk.Menu(self.menu, tearoff=False)
		self.menuAccount = tk.Menu(self.menu, tearoff=False)
		self.menuView    = tk.Menu(self.menu, tearoff=False)

		self.mainframe = None
		self.msglbl    = None

		self.setup()
		self.download_accounts(tracker.account_names)


	def run(self):
		self.root.mainloop()


	def open_account_list_view(self):
		self.mainframe.destroy()
		self.mainframe = AccountListView(self.root, self.tracker, self)
		self.mainframe.grid(row=0, column=0, sticky='nswe')


	def open_account_view(self, account):
		self.mainframe.destroy()
		logging.info(f"Open account '{account.username}'")
		self.mainframe = AccountView(self.root, account, self.tracker)
		self.mainframe.grid(row=0, column=0, sticky='nswe')


	def open_avatar_view(self, account):
		AvatarView(self.root, account)


	def msg(self, text, clear_after=0, fg='#f8f8f8'):
		self.clearmsg()
		self.msglbl = LeftLabel(self.root, text=' '+text, font='Arial 9',
				fg=fg, bg='#303030')
		self.msglbl.grid(row=1, column=0, sticky='nswe')
		if clear_after > 0:
			self.msglbl.after(clear_after*1000, self.clearmsg)

	def clearmsg(self):
		if self.msglbl != None:
			self.msglbl.destroy()


	def setup(self):
		self.menu.configure(background='#303030', foreground='#fefefe')
		self.menu.add_cascade(label='File', menu=self.menuFile)
		self.menu.add_cascade(label='Account', menu=self.menuAccount)
		self.menu.add_cascade(label='View', menu=self.menuView)
		self.menuFile.add_command(label="Delete Avatars Images")
		self.menuFile.add_command(label="Exit", command=self.root.destroy)
		self.menuAccount.add_command(label="Add", command=self.ask_add_account)
		self.menuAccount.add_command(label="Reload All")
		self.menuView.add_command(label="Sort by last commit")
#				command=lambda: self.tracker.sort_accounts('commit'))
		self.menuView.add_command(label="Sort by name")
#				command=lambda: self.tracker.sort_accounts('name', False))
		self.menuView.add_command(label="Sort by number of repos")
#				command=lambda: self.tracker.sort_accounts('repos'))

		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_rowconfigure(0, weight=1)

		# Setup AccountListView first
		self.mainframe = AccountListView(self.root, self.tracker, self)
		self.mainframe.grid(row=0, column=0, sticky='nswe')


	def ask_add_account(self):
		'''
		Callback for menu item 'Account->Add'.
		Ask user for account name and start download thread.
		'''
		acc_name = simpledialog.askstring(parent=self.root, title='Add account',
				prompt='Account Name:')
		if acc_name:
			self.download_accounts([acc_name])

	def download_accounts(self, account_names):
		self.menu.entryconfig('File', state='disabled')
		self.menu.entryconfig('Account', state='disabled')
		self.menu.entryconfig('View', state='disabled')

		logging.info("Starting download thread ...")
		download_thread = AccountDownloader(self, self.tracker,
					account_names)
		download_thread.start()
		self.monitor_download(download_thread)

	def monitor_download(self, thread):
		if thread.is_alive():
			self.root.after(100, lambda: self.monitor_download(thread))
		else:
			logging.info("Download thread done")
			# Add downloaded accounts to tracker.accounts
			self.tracker.accounts += thread.accounts
			self.tracker.sort_accounts('commit')
			self.tracker.store_accounts()
			self.menu.entryconfig('File', state='normal')
			self.menu.entryconfig('Account', state='normal')
			self.menu.entryconfig('View', state='normal')


class AccountDownloader(Thread):
	'''
	Thread for scraping and parsing the account data from https://github.com.
	If an account is parsed, it will be added to AccountListView.
	'''

	def __init__(self, view, tracker, acc_names):
		'''
		Args:
			tracker: GithubTracker instance
			account_names: List with account names to download
		'''
		super().__init__()
		self.T = tracker
		self.V = view
		self.acc_names = acc_names
		self.accounts  = []	# Holds downloaded accounts

		self.pbar = ttk.Progressbar(view.root, orient='horizontal',
				mode='indeterminate', length=200)
		self.pbar.grid(row=2, column=0, sticky='nswe')

	def run(self):
		'''
		Start download thread.
		'''
		tstart = time.time()
		self.pbar.start()
		for i,acc_name in enumerate(self.acc_names):

			# Check if there's already an account with given name
			if self.T.is_account(acc_name):
				self.V.msg(f"Account '{account_name}' already exists")
				continue

			self.V.msg(f'Downloading account {acc_name} ...')
			acc = GithubAccount(acc_name)

			# Scrape and parse account from github.com
			if acc.download(self.T.avatardir):
				self.accounts.append(acc)
				self.V.mainframe.add(acc)

		tend = time.time()
		self.V.msg(f'Done, Time needed: {round(tend-tstart,1)}s', 4)
		self.pbar.after(1000, self.pbar.destroy)

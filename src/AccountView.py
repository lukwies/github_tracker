import tkinter as tk
from PIL import Image,ImageTk
from datetime import datetime
import textwrap

from widgets import *
from util import *

font_col1 = '#090909'
font_col2 = '#151515'
font_col3 = '#454545'

class AccountView(tk.Frame):
	'''
	Frame showing a single github account and its repositories.
	'''

	def __init__(self, parent, account, tracker):

		super().__init__(parent)

		self.account = account
		self.tracker = tracker

		self.sideFrame = Sidebar(self, account, tracker)
		self.repoFrame = RepoList(self, account, tracker)

		self.frBack  = tk.Frame(self, bg='#303030')
		self.btnBack = tk.Button(self.frBack, text='Back', bg='#808080',
					cursor='hand2', command=tracker.view.open_account_list_view,
					highlightthickness=0)
		self.setup()

	def setup(self):
		# Setup menu
		v = self.tracker.view
		v.menu.entryconfig('Account', state='disabled')
		v.menuView.entryconfig('Sort by last commit', state='normal',
			command=lambda: self.sort('commit', True))
		v.menuView.entryconfig('Sort by name', state='normal',
			command=lambda: self.sort('name', False))
		v.menuView.entryconfig('Sort by number of repos', state='disabled')

		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.sideFrame.grid(row=0, column=0, sticky='nswe')
		self.repoFrame.grid(row=0, column=1, sticky='nswe')

		self.btnBack.grid(row=0, column=0, sticky='nswe')
		self.frBack.grid(row=2, column=0, columnspan=2, sticky='nswe')


	def sort(self, by='commit', reverse=False):
		'''
		Sort repositories and refresh screen
		'''
		self.account.sort_repos(by, reverse)
		self.repoFrame.destroy()
		self.repoFrame = RepoList(self, self.account, self.tracker)
		self.repoFrame.grid(row=0, column=1, sticky='nswe')




class Sidebar(tk.Frame):
	'''
	The Sidebar is located at the left side of the screen and shows account
	information like avatar, username, ...
	'''
	def __init__(self, parent, account, tracker):
		super().__init__(parent)
		self.account = account
		self.tracker = tracker
		self.__setup()

	def __setup(self):
		# Avatar image (can be clicked to open avatar view)
		self.img = ImageTk.PhotoImage(Image.open(self.account.avatar_file).resize((180,180)))
		ilbl     = tk.Label(self, image=self.img, cursor='hand2', bg='#424242')
		ilbl.bind('<Button-1>', lambda ev: self.tracker.view.open_avatar_view(self.account))
		ilbl.grid(row=0, column=0, columnspan=2, sticky='nswe', padx=2, pady=2)

		# Account name (can be clicked to open github account with default browser)
		URLLabel(self, self.account.username, 'https://github.com/' + self.account.username,
			font='Arial 15 bold', fg=font_col1).grid(
				row=1, column=0, columnspan=2, sticky='swe', padx=3, pady=5)
		rowi=2

		# Real username (can be empty)
		if self.account.realname != '':
			LeftLabel(self, text=self.account.realname,
				font='Arial 10 bold', fg=font_col1).grid(
				row=rowi, column=0, columnspan=2, sticky='nwe', padx=3)
			rowi += 1

		# Account user location (can be empty)
		if self.account.location != '':
			LeftLabel(self, text='From: ' + self.account.location,
				font='Arial 10', fg=font_col2).grid(
				row=rowi, column=0, columnspan=2, sticky='nswe', padx=3)
			rowi += 1

		# Account description (can be empty)
		if self.account.userinfo != '':
			info = '\n'.join(textwrap.wrap(self.account.userinfo, 30))
			LeftLabel(self, text=info, font='Arial 9', fg=font_col2).grid(
				row=rowi, column=0, columnspan=2, sticky='nwe', padx=3, pady=5)
			rowi += 1

		# Followers (can be clicked to open github follower page in browser)
		URLLabel(self, f'Followers:  {self.account.followers}',
			f'https://github.com/{self.account.username}?tab=followers',
			font='Arial 9', fg=font_col2).grid(
			row=rowi, column=0, columnspan=2, sticky='nswe', padx=3)
		rowi += 1

		# Following (can be clicked to open github following page in browser)
		URLLabel(self, f'Following:  {self.account.following}',
			f'https://github.com/{self.account.username}?tab=following',
			font='Arial 9', fg=font_col2).grid(
				row=rowi, column=0, columnspan=2, sticky='nswe', padx=3)

		self.grid_rowconfigure(10, weight=1)
		self.configure(bg='#424242')


class RepoList(ScrollFrame):
	'''
	The Repository List View is located on the center/right side
	of the screen an shows a list with repositories.
	'''
	def __init__(self, parent, account, tracker):
		super().__init__(parent)
		self.account = account
		self.tracker = tracker
		self.setup()

	def setup(self):
		if len(self.account.repos) > 0:
			for i, repo in enumerate(self.account.repos):
				RepoListItem(self.scroll_frame, repo, self.tracker).grid(
					row=i, column=0, sticky='we')
		else:
			tk.Label(self.scroll_frame, text='No repositories :-(',
				font='Arial 16 bold').grid(row=0, column=0, sticky='nswe')


'''
+---------------+---------------+---------------+
| Repo-Name 	                | language	|
+---------------+---------------+---------------+
| Forked from   | <url>                         |
+---------------+---------------+---------------+
| Description	| <text>			|
+-------+-------+---------------+---------------+
| Last commit:  | 2022-21-2 20:34               |
+---------------+---------------+---------------+
'''
class RepoListItem(tk.Frame):
	'''
	Single Repository item used in RepoList class.
	'''
	def __init__(self, parent, repo, tracker):
		super().__init__(parent)
		self.repo    = repo
		self.tracker = tracker
		self.__setup()

	def __setup(self):
		self.configure(width=400, bg='#ababab', padx=5, pady=3,
				highlightbackground="#323232", highlightthickness=1)
		self.grid_columnconfigure(1, weight=1)

		# Repo name (can be clicked to open github repo in browser)
		URLLabel(self, self.repo['name'], 'https://github.com' + self.repo['url'],
				font='Arial 13 bold', fg=font_col1).grid(
				row=0, column=0, columnspan=2, sticky='nswe')

		# Repo language (Can be empty)
		LeftLabel(self, text=self.repo['language'], font='Arial 8',
			fg=font_col3).grid(row=0, column=2, sticky='nswe', ipadx=3)

		# Date of last commit
		# If repository was commited today, print date in red color.
		d  = self.repo['last_commit']
		fg = '#E00000' if date_is_today(d) else font_col2
		ds = get_time_exceeded(d)

		LeftLabel(self, text='Last commit:', font='Arial 9 bold',
			fg=font_col2).grid(row=1, column=0, sticky='nswe')
		LeftLabel(self, text=ds, font='Arial 8', fg=fg).grid(
				row=1, column=1, columnspan=2, sticky='nswe')
		rowi = 2

		# If repo is a fork, show link of the original repository
		if self.repo['type'] == 'fork':
			LeftLabel(self, text='Forked from:', font='Arial 8 bold',
				fg=font_col2).grid(row=rowi, column=0, sticky='nswe')

			URLLabel(self, self.repo['forked_from'], 'https://github.com' + self.repo['forked_from'],
				font='Arial 8').grid(row=rowi, column=1, columnspan=2, sticky='nswe')
			rowi += 1

		# Account description text (Can be empty)
		if self.repo['description'] != '':
			info = '\n'.join(textwrap.wrap(self.repo['description'], 100))
			LeftLabel(self, text=info, font='Arial 8', fg=font_col2).grid(
				row=rowi, column=0, columnspan=3, sticky='nswe')
			rowi += 1

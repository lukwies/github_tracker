import tkinter as tk
from PIL import Image,ImageTk
from datetime import datetime
import textwrap

from widgets import *
from util import *

font8  = 'Arial 8'
font8b = 'Arial 8 bold'

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
		self.repoFrame = RepoList(self, account)

		self.lblurl  = None
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

		self.frBack.grid(row=3, column=0, columnspan=2, sticky='nswe')
		self.btnBack.grid(row=0, column=0, sticky='nswe')


	def sort(self, by='commit', reverse=False):
		'''
		Sort repositories and refresh screen
		'''
		self.account.sort_repos(by, reverse)
		self.repoFrame.destroy()
		self.repoFrame = RepoList(self, self.account)
		self.repoFrame.grid(row=0, column=1, sticky='nswe')

	def url_label_open(self, url):
		'''
		Show url label on AccountView frame.
		This is used to show the complete url while a user
		is mouse hovering an URLLabel.
		'''
		if not self.lblurl:
			self.lblurl = LeftLabel(self, text=url,
				font='Arial 9', bg='#b5b5b5',
				highlightbackground="#525252",
				highlightthickness=1)
			self.lblurl.grid(row=1, column=0, ipadx=3,
				columnspan=2, sticky='nswe')

	def url_label_close(self, url):
		'''
		Hide url label from AccountView frame.
		'''
		if self.lblurl:
			self.lblurl.destroy()
			self.lblurl = None



class Sidebar(tk.Frame):
	'''
	The Sidebar is located at the left side of the screen and shows account
	information like avatar, username, ...
	'''
	def __init__(self, parent, account, tracker):
		super().__init__(parent)
		self.account = account
		self.parent  = parent
		self.__setup()

	def __setup(self):
		# Avatar image (can be clicked to open avatar view)
		self.img = ImageTk.PhotoImage(Image.open(self.account.avatar_file).resize((180,180)))
		ilbl     = tk.Label(self, image=self.img, cursor='hand2', bg='#424242')
		ilbl.bind('<Button-1>', lambda ev: self.tracker.view.open_avatar_view(self.account))
		ilbl.grid(row=0, column=0, columnspan=2, sticky='nswe', padx=2, pady=2)

		# Account name (Click to open github account in browser)
		MyURLLabel(self, 'https://github.com/'+self.account.username,
			self.parent, text=self.account.username,
			font='Arial 15 bold', fg=font_col1).grid(row=1,
			column=0, columnspan=2, sticky='swe', padx=3, pady=5)
		rowi=2

		# Real username (can be empty)
		if self.account.realname != '':
			LeftLabel(self, text=self.account.realname,
				font='Arial 10 bold', fg=font_col1).grid(
				row=rowi, column=0, columnspan=2,
				sticky='nwe', padx=3)
			rowi += 1

		# Account user location (can be empty)
		if self.account.location != '':
			LeftLabel(self, text='From: '+self.account.location,
				font='Arial 10', fg=font_col2).grid(
				row=rowi, column=0, columnspan=2,
				sticky='nswe', padx=3)
			rowi += 1

		# Account description (can be empty)
		if self.account.userinfo != '':
			info = '\n'.join(textwrap.wrap(
				self.account.userinfo, 30))
			LeftLabel(self, text=info, font='Arial 9',
				fg=font_col2).grid(row=rowi, column=0,
				columnspan=2, sticky='nwe', padx=3, pady=5)
			rowi += 1

		# Followers (Click to open github follower page in browser)
		if self.account.followers > 0:
			s   = "Followers: {}".format(self.account.followers)
			url = "https://github.com/{}?tab=followers".format(
				self.account.username)
			MyURLLabel(self, url, self.parent, text=s,
				font='Arial 9', fg=font_col2).grid(
				row=rowi, column=0, columnspan=2,
				sticky='nswe', padx=3)
			rowi += 1

		# Following (Click to open github following page in browser)
		if self.account.following > 0:
			s   = "Following: {}".format(self.account.following)
			url = "https://github.com/{}?tab=following".format(
				self.account.username)
			MyURLLabel(self, url, self.parent, text=s, font='Arial 9',
				fg=font_col2).grid(row=rowi, column=0,
				columnspan=2, sticky='nswe', padx=3)
			rowi += 1

		self.grid_rowconfigure(10, weight=1)
		self.configure(bg='#b8b8b8')


class RepoList(ScrollFrame):
	'''
	The Repository List View is located on the center/right side
	of the screen an shows a list with repositories.
	'''
	def __init__(self, parent, account):
		super().__init__(parent)
		self.account = account
		self.aview   = parent
		self.setup()

	def setup(self):
		if len(self.account.repos) > 0:
			for i, repo in enumerate(self.account.repos):
				RepositoryView(self.scroll_frame,
#				RepoListItem(self.scroll_frame,
					self.account, repo,
					self.aview).grid(
					row=i, column=0, sticky='we')
		else:
			tk.Label(self.scroll_frame,
				text='No repositories :-(',
				font='Arial 16 bold').grid(
				row=0, column=0, sticky='nswe')


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
class RepositoryView(tk.Frame):
	'''
	Single Repository item used in RepoList class.
	'''
	def __init__(self, parent, account, repo, aview):
		super().__init__(parent)
		self.account = account
		self.repo    = repo
		self.aview   = aview
		self.expand  = None	# RepositoryExpandView
		self.btnExp  = None	# Button to expand view
		self.setup()

	def setup(self):
		self.configure(width=400, bg='#ababab', padx=3,
			pady=3, highlightbackground="#909090",
			highlightthickness=1)
		self.grid_columnconfigure(1, weight=1, minsize=300)

		# Frame holding the header of the repository list item.
		fr = tk.Frame(self, height=24)

		# Repo name (can be clicked to open repo in browser)
		lbl = MyURLLabel(fr, 'https://github.com'+self.repo['url'],
			self.aview, text=self.repo['name'], font='Arial 13 bold',
			fg=font_col1)
		lbl.place(y=0, x=0)

		# Repo language (Can be empty)
		x=lbl.winfo_reqwidth()
		txt = "("+self.repo['language']+")"  if self.repo['language']  != '' else ''
		LeftLabel(fr, text=txt,	font=font8, fg=font_col3).place(y=5, x=x)

		fr.grid(row=0, column=0, columnspan=2, sticky='nsew')

		# Button to expand repo info
		self.btnExp = ButtonLabel(self, command=self.handle_expand,
			text='V', font='Arial 6 bold')
		self.btnExp.grid(row=0, column=2, sticky='ne')

		# Date of last commit.
		# If repository was commited today, user red color.
		d  = self.repo['last_commit']
		fg = '#E00000' if date_is_today(d) else font_col2
		ds = get_time_exceeded(d)
		LeftLabel(self, text='Last commit:', font=font8b,
			fg=font_col2).grid(row=1, column=0, sticky='nswe')
		LeftLabel(self, text=ds, font=font8, fg=fg).grid(
				row=1, column=1, columnspan=2, sticky='nswe')


	def handle_expand(self):
		if not self.expand:
			self.expand = RepositoryExpandView(self)
			self.expand.grid(row=3, column=0, sticky='nswe', columnspan=3)
			self.btnExp.configure(text='X')
		else:
			self.btnExp.configure(text='V')
			self.expand.destroy()
			self.expand = None

class RepositoryExpandView(tk.Frame):
	'''
	Expanding part of the RepositoryView.
	'''

	def __init__(self, parent):
		super().__init__(parent)
		self.repo    = parent.repo
		self.aview   = parent.aview
		self.account = parent.account
		self.bg      = '#c5c5c5'
		self.fg      = '#121212'
		self.setup()

	def setup(self):

		self.configure(bg=self.bg)
		self.grid_columnconfigure(1, weight=1)

		rowi=0
		# If repo is a fork, show link to the original repository
		if self.repo['type'] == 'fork':
			LeftLabel(self, text='Forked from:',
				font=font8b, fg=self.fg).grid(
				row=rowi, column=0, sticky='nswe')

			MyURLLabel(self,
				'https://github.com'+self.repo['forked_from'],
				self.aview, text=self.repo['forked_from'],
				font=font8).grid(row=rowi, column=1,
				sticky='nswe')
			rowi += 1

		# If repo has been forked by others, show number of forks
		if self.repo['num_forks'] > 0:
			LeftLabel(self, text='Fork Count:', font=font8b,
				fg=self.fg).grid(row=rowi, column=0,
				sticky='nswe')

			url = "https://github.com/{}/{}/network/members".format(
				self.account.username, self.repo['name'])
			s = "{}".format(self.repo['num_forks'])

			MyURLLabel(self, url, self.aview, text=s, font=font8).grid(
				row=rowi, column=1, sticky='nswe')
			rowi += 1

		# Account description text (Can be empty)
		if self.repo['description'] != '':
			info = '\n'.join(textwrap.wrap(
				self.repo['description'], 100))
			LeftLabel(self, text=info, font=font8, fg='black', bg=self.bg).grid(
				row=rowi, column=0, columnspan=2,
				sticky='nsw', ipadx=5, ipady=3)
			rowi += 1


class MyURLLabel(URLLabel):
	'''
	Url label which opens another label on mouse hovering.
	'''
	def __init__(self, parent, url, aview, *args, **kwargs):
		super().__init__(parent, url, *args, **kwargs)

		self.url   = url
		self.aview = aview

		self.bind('<Enter>', self.on_enter)
		self.bind('<Leave>', self.on_leave)

	def on_enter(self, ev):
		self.enter(ev)
		self.aview.url_label_open(self.url)

	def on_leave(self, ev):
		self.leave(ev)
		self.aview.url_label_close(self.url)

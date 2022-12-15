import tkinter as tk
from PIL import Image,ImageTk
from widgets import *
import textwrap
from datetime import datetime


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
					cursor='hand2', command=tracker.view.open_account_list_view)
		self.__setup()

	def __setup(self):
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.sideFrame.grid(row=0, column=0, sticky='nswe')
		self.repoFrame.grid(row=0, column=1, sticky='nswe')

		self.btnBack.grid(row=0, column=0, sticky='nswe')
		self.frBack.grid(row=2, column=0, columnspan=2, sticky='nswe')



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
		self.img = ImageTk.PhotoImage(Image.open(self.account.avatar_file).resize((180,180)))
		tk.Label(self, image=self.img).grid(row=0, column=0, columnspan=2, sticky='nw', padx=3, pady=3)

		URLLabel(self, self.account.username, 'https://github.com/' + self.account.username,
				font='Arial 14 bold').grid(row=1, column=0, columnspan=2, sticky='swe', padx=3)
		rowi=2

		if self.account.realname != '':
			make_label(self, self.account.realname, 'Arial 9', 'grey').grid(
					row=rowi, column=0, columnspan=2, sticky='nwe', padx=3)
			rowi += 1

		if self.account.location != '':
			make_label(self, 'Location: ' + self.account.location, 'Arial 10', 'grey').grid(
					row=rowi, column=0, columnspan=2, sticky='nswe', padx=3)
			rowi += 1

		if self.account.userinfo != '':
			info = '\n'.join(textwrap.wrap(self.account.userinfo, 30))
			make_label(self, info, 'Arial 9').grid(
					row=rowi, column=0, columnspan=2, sticky='nwe', padx=3, pady=5)
			rowi += 1

		s = f'Followers: {self.account.followers}\nFollowing: {self.account.following}'
		LeftLabel(self, text=s).grid(row=rowi, column=0, columnspan=2, sticky='nswe', padx=3)
		rowi += 1

		self.grid_rowconfigure(6, weight=1)
		self.configure(bg='#535353')


class RepoList(ScrollFrame):
	'''
	The Repository List View is located on the center/right side
	of the screen an shows a list with repositories.
	'''
	def __init__(self, parent, account, tracker):
		super().__init__(parent)
		self.account = account
		self.tracker = tracker
		self.__setup()

	def __setup(self):
		if len(self.account.repos) > 0:
			for i, repo in enumerate(self.account.repos):
				RepoListItem(self.scroll_frame, repo, self.tracker).grid(
					row=i, column=0, sticky='we')
		else:
			tk.Label(self.scroll_frame, text='No repositories :-(',
				font='Arial 12 bold').grid(row=0, column=0, sticky='nswe')

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

		URLLabel(self, self.repo['name'], 'https://github.com' + self.repo['url'],
				font='Arial 12 bold').grid(row=0, column=0, columnspan=2, sticky='nswe')
		make_label(self, self.repo['language'], 'Arial 8', '#989898').grid(
				row=0, column=2, sticky='nswe')

		make_label(self, 'Last commit:', 'Arial 8 bold').grid(
			row=1, column=0, sticky='nswe')

		# If repository was commited today, print red date
		d = self.repo['last_update']
		if d.date() == datetime.today().date():
			LeftLabel(self, text=d.strftime('%c'), font='Arial 8 bold',
				fg='#E00000').grid(
				row=1, column=1, columnspan=2, sticky='nswe')
		else:
			LeftLabel(self, text=d.strftime('%c'), font='Arial 8').grid(
				row=1, column=1, columnspan=2, sticky='nswe')

		rowi = 2

		if self.repo['type'] == 'fork':
			make_label(self, 'Forked from:', 'Arial 8 bold').grid(
				row=rowi, column=0, sticky='nswe')

			URLLabel(self, self.repo['forked_from'], 'https://github.com' + self.repo['forked_from'],
				font='Arial 8').grid(row=rowi, column=1, columnspan=2, sticky='nswe')
			rowi += 1

		if self.repo['description'] != '':
			make_label(self, self.repo['description'], 'Arial 8').grid(
				row=rowi, column=0, columnspan=3, sticky='nswe')
			rowi += 1



## TODO REMOVE
def make_label(parent, text, font, fg='black'):
	return tk.Label(parent, text=text, font=font, fg=fg, justify='left', anchor='w')


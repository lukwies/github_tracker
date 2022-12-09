import tkinter as tk
from PIL import Image,ImageTk
from widgets import *
import textwrap
#from AccountListFrame import *



class AccountView(tk.Frame):
	'''
	Frame showing a single Account.
	'''

	def __init__(self, parent, account, tracker):
		'''
		Account list view.

		Args:
			tracker: GithubTracker instance
		'''
		super().__init__(parent)

		self.account = account
		self.tracker = tracker

		self.sideFrame = Sidebar(self, account, tracker)
		self.repoFrame = RepoList(self, account, tracker)
		self.__setup()

	def __setup(self):
		self.grid_columnconfigure(1, weight=1)
		self.sideFrame.grid(row=0, column=0, sticky='nswe')
		self.repoFrame.grid(row=0, column=1, sticky='nswe')



class Sidebar(tk.Frame):
	def __init__(self, parent, account, tracker):
		super().__init__(parent)
		self.account = account
		self.tracker = tracker
		self.__setup()

	def __setup(self):
		self.img = ImageTk.PhotoImage(Image.open(self.account.avatar_file).resize((160,160)))
		tk.Label(self, image=self.img).grid(row=0, column=0, columnspan=2, sticky='nw')

		URLLabel(self, self.account.username, 'https://github.com/' + self.account.username,
				font='Arial 12 bold').grid(row=1, column=0, columnspan=2, sticky='nswe')
		rowi=2

		if self.account.realname != '':
			make_label(self, self.account.realname, 'Arial 11').grid(
					row=rowi, column=0, columnspan=2, sticky='nswe')
			rowi += 1

		if self.account.location != '':
			make_label(self, self.account.location, 'Arial 10').grid(
					row=rowi, column=0, columnspan=2, sticky='nswe')
			rowi += 1

		if self.account.userinfo != '':
			info = '\n'.join(textwrap.wrap(self.account.userinfo, 30))
			make_label(self, info, 'Arial 9').grid(
					row=rowi, column=0, columnspan=2, sticky='nswe')
			rowi += 1

		self.grid_columnconfigure(0, minsize=160)
		self.grid_rowconfigure(4, weight=1)
		self.configure(bg='#939393')


class RepoList(tk.Frame):
	def __init__(self, parent, account, tracker):
		super().__init__(parent)
		self.account = account
		self.tracker = tracker
		self.__setup()

	def __setup(self):
		self.configure(width=300, bg='#ababab')
		self.grid_columnconfigure(0, weight=1)

		for i, repo in enumerate(self.account.repos):
			RepoListItem(self, repo, self.tracker).grid(
				row=i, column=0, sticky='nswe')
			if i == 4:
				break


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
	def __init__(self, parent, repo, tracker):
		super().__init__(parent)
		self.repo    = repo
		self.tracker = tracker
		self.__setup()

	def __setup(self):
		self.configure(width=300, bg='#ababab', padx=5, pady=3,
				highlightbackground="#323232", highlightthickness=1)
		self.grid_columnconfigure(1, weight=1)

		URLLabel(self, self.repo['name'], 'https://github.com' + self.repo['url'],
				font='Arial 10 bold').grid(row=0, column=0, columnspan=2, sticky='nswe')
		make_label(self, self.repo['language'], 'Arial 8', '#989898').grid(
				row=0, column=2, sticky='nswe')

		make_label(self, 'Last commit:', 'Arial 8 bold').grid(
			row=1, column=0, sticky='nswe')
		make_label(self, self.repo['last_update'].strftime('%c'), 'Arial 8').grid(
			row=1, column=1, columnspan=2, sticky='nswe')

		rowi = 2

		if self.repo['type'] == 'fork':
			make_label(self, 'Forked from:', 'Arial 8 bold').grid(
				row=rowi, column=0, sticky='nswe')

			URLLabel(self, self.repo['forked_from'], 'https://github.com' + self.repo['forked_from'],
				font='Arial 8').grid(row=rowi, column=1, columnspan=2, sticky='nswe')

#			make_label(self, self.repo['forked_from'], 'Arial 8').grid(
#				row=rowi, column=1, columnspan=2, sticky='nswe')
			rowi += 1

		if self.repo['description'] != '':
			make_label(self, self.repo['description'], 'Arial 8').grid(
				row=rowi, column=0, columnspan=3, sticky='nswe')
			rowi += 1




def make_label(parent, text, font, fg='black'):
	return tk.Label(parent, text=text, font=font, fg=fg, justify='left', anchor='w')

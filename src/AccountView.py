import tkinter as tk
from PIL import Image,ImageTk
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
		self.img = ImageTk.PhotoImage(Image.open(self.account.avatar_file).resize((140,140)))
		tk.Label(self, image=self.img).grid(row=0, column=0, columnspan=2, sticky='nswe')

		make_label(self, self.account.username, 'Arial 12 bold').grid(
				row=1, column=0, columnspan=2, sticky='nswe')

		make_label(self, self.account.realname, 'Arial 11').grid(
				row=2, column=0, columnspan=2, sticky='nswe')

		make_label(self, self.account.location, 'Arial 10').grid(
				row=3, column=0, columnspan=2, sticky='nswe')

		self.configure(bg='#676767', width=200)

class RepoList(tk.Frame):
	def __init__(self, parent, account, tracker):
		super().__init__(parent)
		self.account = account
		self.tracker = tracker
		self.__setup()

	def __setup(self):
		self.configure(width=300, bg='#ababab')


'''
+-------+-------+-------+-------+-------+-------+
| Repo-Name					|
+-------+-------+-------+-------+-------+-------+
| 


'''
class RepoListItem(tk.Frame):
	def __init__(self, parent, repo, tracker):
		super().__init__(parent)
		self.repo    = repo
		self.tracker = tracker
		self.__setup()

	def __setup(self):
		self.configure(width=300, bg='#ababab')

		make_label(self, self.repo['name'], 'Arial 10 bold')







def make_label(parent, text, font, fg='black'):
	return tk.Label(parent, text=text, font=font, fg=fg, justify='left', anchor='w')

import tkinter as tk
from AccountListView import *
#from AccountView import *

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

		self.mainframe = AccountListView(self.root, tracker)
		self.mainframe.pack(fill='x')

		self._setup()


	def run(self):
		self.root.mainloop()


	def open_account_list_view(self):
		self.mainframe = AccountListView(self.root, tracker)
		self.mainframe.pack(fill='x')


	def open_accout_view(self, account):
		self.mainframe = AccountView(self.root, tracker)
		self.mainframe.pack(fill='x')


	def _setup(self):
		self.menu.configure(background='#303030', foreground='#fefefe')
		self.menu.add_cascade(label='File', menu=self.menuFile)
		self.menu.add_cascade(label='File', menu=self.menuAccount)
		self.menuFile.add_command(label="Exit", command=self.root.destroy)
		self.root.grid_columnconfigure(0, weight=1)




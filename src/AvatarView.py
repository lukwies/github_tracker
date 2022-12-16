import tkinter as tk
#import tkinter.ttk as ttk

from PIL import Image,ImageTk


class AvatarView(tk.Toplevel):

	def __init__(self, parent, account):
		'''
		Simple screen to view the account avatar image real size.

		Args:
			parent:  Parent tkinter widget
			account: GithubAccount instance
		'''

		super().__init__(parent)
		self.account = account

		self.title(f'Avatar of {account.username}')

		self.img    = ImageTk.PhotoImage(Image.open(account.avatar_file)) #.resize((75,75)))
		self.avatar = tk.Label(self, image=self.img)
		self.avatar.pack(fill='both', expand=True)
		self.avatar.configure(highlightbackground="#626262", highlightthickness=1)

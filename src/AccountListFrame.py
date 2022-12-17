import tkinter as tk
from PIL import Image,ImageTk
import webbrowser
from widgets import *
from util import *
from tkinter.messagebox import askyesno


#
# +—————————————-———————————————————————————————————————+
# |+-----+ NickName					|
# ||     | Last Commit:					|
# ||     | Last Repo:					|
# |+-----+ Repo Count:					|
# +—————————————————————————————————————————————————————+
#
'''
     0      1       2       3       4
  +-----+-------+-------+-------+-------+
0 |<img>| Nickname	|	| <btn> |
  +	+-------+-------+-------+-------+
1 |	|Repos: | <n>	|	|	|
  +	+-------+-------+-------+-------+
2 |	|Commit:| <date>|	|	|
  +	+-------+-------+-------+-------+
3 |	|	|	|	|	|
  +-----+-------+-------+-------+-------+

'''



class AccountListFrame(tk.Frame):

	def __init__(self, parent, account, tracker):
		super().__init__(parent)
		self.account   = account
		self.tracker   = tracker
		self.avatar    = tk.Label(self)
		self.setup()


	def setup(self):
		self.configure(width=400, bg='#a0a0b0', padx=3, pady=3,
			highlightbackground="#909090", highlightthickness=1)
		self.grid_columnconfigure(0, weight=1, minsize=300)

		fr = tk.Frame(self, height=85, cursor='hand2')
		fr.bind('<Button-1>', self.open_account)


		# Avatar image (Click to open avatar view)
		self.img = ImageTk.PhotoImage(Image.open(
				self.account.avatar_file).resize((75,75)))
		self.avatar = tk.Label(fr, width=75, height=75,
				image=self.img, cursor='hand2', bg='#323232')
		self.avatar.bind('<Button-1>', lambda ev: self.tracker.view.open_avatar_view(self.account))
		self.avatar.configure(highlightbackground="#323232", highlightthickness=1)
		self.avatar.place(y=3, x=3)

		# Account username
		self.lbl(fr, text=self.account.username, font='Arial 14 bold').place(y=2, x=85)


		if len(self.account.repos) > 0:

			# Print last commit in other color if commit date was today.
			self.lbl(fr, text='Last Commit:', font='Arial 9 bold').place(y=32, x=85)
			sdate = get_time_exceeded(self.account.last_commit)

			if self.account.commited_today():
				l = self.lbl(fr, text=sdate, font='Arial 9 bold',
					fg='red').place(y=32, x=170)
			else:
				l = self.lbl(fr, text=sdate, font='Arial 9').place(y=32, x=170)

			# Last commited repo
			self.lbl(fr, text='Last Repo:', font='Arial 9 bold').place(y=47, x=85)
			self.lbl(fr, text=self.account.repos[0]['name'],
				font='Arial 9').place(y=47, x=170)

			# Number of repositories
			self.lbl(fr, text='Repo Count:', font='Arial 9 bold').place(y=62, x=85)
			self.lbl(fr, text=str(len(self.account.repos)), font='Arial 9').place(y=62, x=170)

		fr.grid(row=0, column=0, sticky='nswe')

		# Buttons
		fr2 = tk.Frame(self, height=85, width=25)
		btn = ButtonLabel(fr2, command=lambda: self.confirm_and_delete(self.account),
				text='X', fg='red')
		btn.set_color('#410000', '#eebbbb')
		btn.set_hover_color('#550000', '#cc0000')
		btn.place(y=3, x=3, width=20)
		fr2.grid(row=0, column=1, sticky='nswe')


	def lbl(self, parent, *args, **kwargs):
		lbl = LeftLabel(parent, *args, **kwargs)
		return lbl

	def open_account(self, ev):
		self.tracker.view.open_account_view(self.account)


	def confirm_and_delete(self, account):
		yes = askyesno(title='Delete Account',
			message=f'Do you really want to delete {account.username}?')
		if yes:
			self.tracker.delete_account(account)
			self.tracker.view.open_account_list_view()



















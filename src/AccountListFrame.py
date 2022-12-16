import tkinter as tk
from PIL import Image,ImageTk
import webbrowser
from widgets import *
from util import *
from tkinter.messagebox import askyesno


#
# +—————————————————————————————————————————————————————+
# |+------+						|
# ||      | NickName					|
# ||      | RealName					|
# ||      | Repos: 32					|
# |+------+ Last commit: 2022-12-3 22:34		|
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
		self.btnDelete = tk.Button(self, text='X', font='Arial 7', fg='red',
					command=lambda: self._confirm_and_delete(account))
		self.__setup()


	def __setup(self):
		self.configure(bg='#bcbcbc', padx=5, pady=3, highlightbackground="#323232", highlightthickness=1)
		self.grid_columnconfigure(1, weight=1)

		# Avatar image (Click to open avatar view)
		self.img    = ImageTk.PhotoImage(Image.open(self.account.avatar_file).resize((75,75)))
		self.avatar = tk.Label(self, width=75, height=75, image=self.img, cursor='hand2')
		go_back = lambda ev: self.tracker.view.open_avatar_view(self.account)
		self.avatar.bind('<Button-1>', go_back)
#		self.avatar.configure(highlightbackground="#626262", highlightthickness=1)
		self.avatar.grid(row=0, column=0, rowspan=4, sticky='nw')

		# Labels
		self.lbls = self._get_labelpanel()
		self.lbls.grid(row=0, column=1, rowspan=4, sticky='nswe', padx=5)

		# Buttons
		self.btnDelete.grid(row=0, column=2, sticky='nw')
		self.btnDelete.configure(highlightbackground='#bcbcbc',
			highlightthickness=1)


	def _get_labelpanel(self):
		win = tk.PanedWindow(self, cursor='hand2', bg='#f9f9f9')
		win.grid_columnconfigure(1, weight=1)

		self._lbl(win, '#D5D5D5', text=self.account.username, font='Arial 12 bold').grid(
			row=0, column=0, sticky='nswe', columnspan=2)

		if len(self.account.repos) > 0:

			self._lbl(win, text='Last Commit:', font='Arial 9 bold').grid(
				row=1, column=0, sticky='nswe')

			# Print last commit in other color if commit date was today.
			sdate = get_time_exceeded(self.account.last_commit)
			if self.account.commited_today():
				l = self._lbl(win, text=sdate, font='Arial 8 bold', fg='red').grid(
					row=2, column=1, sticky='nswe')
			else:
				l = self._lbl(win, text=sdate, font='Arial 8').grid(
					row=2, column=1, sticky='nswe')

#			self._lbl(win, text='Last Repo:', font='Arial 8 bold').grid(
#				row=2, column=0, sticky='nswe')
			self._lbl(win, text=self.account.repos[0]['name'], font='Arial 9').grid(
				row=1, column=1, sticky='nswe')

			self._lbl(win, text='Repositories:', font='Arial 9 bold').grid(
				row=3, column=0, sticky='nswe')
			self._lbl(win, text=str(len(self.account.repos)), font='Arial 9').grid(
				row=3, column=1, sticky='nswe')

#			URLLabel(win, 'Link', 'https://github.com').grid(row=4, column=0, sticky='nswe')

		return win


	def _lbl(self, parent, bg='#f9f9f9', *args, **kwargs):
		lbl = LeftLabel(parent, bg=bg, *args, **kwargs)
		lbl.bind('<Button-1>', self._open_account)
		return lbl

	def _open_account(self, ev):
		self.tracker.view.open_account_view(self.account)


	def _confirm_and_delete(self, account):
		yes = askyesno(title='Delete Account',
			message=f'Do you really want to delete {account.username}?')
		if yes:
			self.tracker.delete_account(account)
			self.tracker.view.open_account_list_view()

import tkinter as tk
from PIL import Image,ImageTk
import webbrowser
from widgets import URLLabel
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

		# Avatar image
		self.img    = ImageTk.PhotoImage(Image.open(self.account.avatar_file).resize((70,70)))
		self.avatar = tk.Label(self, width=70, height=70, image=self.img)
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
		win = tk.PanedWindow(self, cursor='hand2')
		win.grid_columnconfigure(1, weight=1)

		self._lbl(win, self.account.username, 'Arial 11 bold').grid(row=0, column=0, sticky='nswe', columnspan=2)

		if len(self.account.repos) > 0:
			self._lbl(win, 'Repos:', 'Arial 8 bold').grid(row=1, column=0, sticky='nswe')
			self._lbl(win, str(len(self.account.repos)), 'Arial 8').grid(row=1, column=1, sticky='nswe')

			self._lbl(win, 'Last Commit:', 'Arial 8 bold').grid(row=2, column=0, sticky='nswe')
			self._lbl(win, self.account.repos[0]['last_update'].strftime('%Y-%m-%d %H:%S'), 'Arial 8').grid(
					row=2, column=1, sticky='nswe')

			self._lbl(win, 'Last Repo:', 'Arial 8 bold').grid(row=3, column=0, sticky='nswe')
			self._lbl(win, self.account.repos[0]['name'], 'Arial 8').grid(row=3, column=1, sticky='nswe')

#			URLLabel(win, 'Link', 'https://github.com').grid(row=4, column=0, sticky='nswe')

		return win


	def _lbl(self, parent, text, font='Arial 10 bold'):
		lbl = tk.Label(parent, text=text, font=font,
				justify='left', anchor='w', padx=5)
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

import tkinter as tk
import webbrowser

class URLLabel(tk.Label):
	'''
	Label which can be clicked to open an URL within the default webbrowser.
	'''
	def __init__(self, parent, text, url, font='Arial 8', fg='black', fg_hover='blue', **kwargs):
		super().__init__(parent, text=text, font=font, fg=fg, cursor='hand2')

		self.fg_      = fg
		self.fg_hover = fg_hover
		self.url      = url

		self.bind('<Enter>', self.enter)
		self.bind('<Leave>', self.leave)
		self.bind('<Button-1>', self.openURL)

		self.configure(justify='left', anchor='w')

	def enter(self, ev):
		self.configure(fg=self.fg_hover)

	def leave(self, ev):
		self.configure(fg=self.fg_)

	def openURL(self, ev):
		webbrowser.open_new_tab(self.url)


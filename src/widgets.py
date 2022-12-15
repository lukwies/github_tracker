import tkinter as tk
from tkinter import ttk
import webbrowser

class ScrollFrame(ttk.Frame):
	'''
	Scrollable frame.
	NOTE: If you want to use this class, remember to place things
	inside self.scrollable_frame, and not directly into an object of this class:

		frame = ScrollableFrame(root)

		for i in range(50):
			ttk.Label(frame.scrollable_frame, text="Sample scrolling label").pack()
	'''
	def __init__(self, container, *args, **kwargs):
		super().__init__(container, *args, **kwargs)
		self.canvas = tk.Canvas(self)
		self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
		self.scroll_frame = ttk.Frame(self.canvas)

		self.scroll_frame.bind(
			"<Configure>",
			lambda e: self.canvas.configure(
				scrollregion=self.canvas.bbox("all")
			)
		)

		self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
		self.canvas.configure(yscrollcommand=self.scrollbar.set)

		self.canvas.pack(side="left", fill="both", expand=True)
		self.scrollbar.pack(side="right", fill="y")

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


class LeftLabel(tk.Label):
	'''
	Left justified label
	'''
	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		self.configure(anchor='w', justify='left')


class ClickableLeftLabel(tk.Label):
	'''
	Clickable left justified label
	'''
	def __init__(self, parent, command, fg_hover='blue', *args, **kwargs):
		super().__init__(parent, cursor='hand2', *args, **kwargs)
		self.configure(anchor='w', justify='left')
		self.bind('<Button-1>', command)

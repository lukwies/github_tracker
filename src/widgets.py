import tkinter as tk
from tkinter import ttk
import webbrowser
from tkinter import font

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
	On mouse hover the font color will change to self.fg_hover and the text
	will shown underlined.
	'''
	def __init__(self, parent, url, *args, **kwargs):
		'''
		Args:
			parent:  Parent widget
			url:     Url to open in browser
			kwargs:  Arguments, passed to tk.Label()
		NOTE:
		'''
		super().__init__(parent, cursor='hand2', *args, **kwargs)

		self.url = url

		self.bind('<Enter>',    self.enter)
		self.bind('<Leave>',    self.leave)
		self.bind('<Button-1>', self.openURL)
		self.configure(justify='left', anchor='w')
#			fg='#0000ea')

	def enter(self, ev):
		f = font.Font(self, self.cget("font"))
		f.configure(underline=True)
		self.configure(font=f)

	def leave(self, ev):
		f = font.Font(self, self.cget("font"))
		f.configure(underline=False)
		self.configure(font=f)

	def openURL(self, ev):
		webbrowser.open_new_tab(self.url)



class LeftLabel(tk.Label):
	'''
	Left justified label
	'''
	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		self.configure(anchor='w', justify='left')


class ButtonLabel(tk.Label):
	'''
	Clickable label
	'''
	def __init__(self, parent, command=None, *args, **kwargs):
		super().__init__(parent, cursor='hand2', *args, **kwargs)
		self.cmd = command

		self.bg  = '#c8c8c8'
		self.fg  = '#323232'
		self.bg2 = '#999999'
		self.fg2 = '#121212'

		self.setup()


	def set_color(self, fg, bg):
		self.configure(fg=fg, bg=bg)
		self.bg = bg
		self.fg = fg

	def set_hover_color(self, fg, bg):
		self.bg2 = bg
		self.fg2 = fg


	def setup(self):
		self.configure( #anchor='w', justify='left',
			fg=self.fg, bg=self.bg,
			highlightbackground="#626262",
			highlightthickness=1)
		self.bind('<Button-1>', self._on_click)
		self.bind('<Enter>', self._on_enter)
		self.bind('<Leave>', self._on_leave)

	def _on_click(self, ev):
		if self.cmd:
			self.cmd()

	def _on_enter(self, ev):
		self.configure(fg=self.fg2, bg=self.bg2)

	def _on_leave(self, ev):
		self.configure(fg=self.fg, bg=self.bg)


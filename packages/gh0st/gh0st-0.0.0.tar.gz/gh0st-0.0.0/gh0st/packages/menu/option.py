import curses

class option():
	def __init__(self, title, action=None, selected=False, size=(8,8), coord=(0,0), controls={}):
		self.title=title
		self.action=action	# Function call to initiate
		self.selected=selected
		self.size=size
		self.coord=coord

		self.parent_window=None
		self.window=None	# set from parent window, or self.arrange()
		if self.parent_window is not None:
			self.window=parent_window.derwin(*size, *coord)
		self.controls={}
		self.controls.update(controls)	# setting this directly makes this behave staticly O.o
		self.controls['select']=action	# {up_keys:None, down_keys:None, left_keys:None, right_keys:None, select_keys:self.action}	# direction controls and actions

	def __str__(self):
		if self.selected:
			return f">{self.title}<".center(8)
		return self.title.center(8)
	def __repr__(self):
		string="\n-----OPTION-------\n"
		# for attr in dir(self):
		# 	if not callable(getattr(self,attr)):	# try to only print parameters
		# 		string+=f"{attr}:{getattr(self,attr)}\n"
		string += f"title:    {self.title}\n"
		string += f"action:   {self.action}\n"
		string += f"selected: {self.selected}\n"
		string += f"size:     {self.size}\n"
		string += f"coord:    {self.coord}\n"
		string += f"controls:\n"
		for k,v in self.controls.items():
			try:
				string += f"\t{k}: {v.title}\n"
			except:
				string += f"\t{k}: {repr(v)}\n"
		string += "\n-----END-OPTION-------\n"
		return string
	def arrange(self, win, size, coord):
		self.parent_window=win
		self.window=win.derwin(*size, *coord)
		self.size=size
		self.coord=coord
		self.draw()

	def toggle(self):
		if self.selected:
			self.window.erase()
			self.window.addstr(1,1,self.title)
			self.selected=False
		else:
			self.window.box()
			self.selected=True
		self.window.refresh()

	def draw(self):
		if self.selected:
			self.window.box()
		# self.window.addstr(1,1,self.title)
		self.window.addstr(1,1,self.title.center(self.size[1]-2))
		self.window.refresh()
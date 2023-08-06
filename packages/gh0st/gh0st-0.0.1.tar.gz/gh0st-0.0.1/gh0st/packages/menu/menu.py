import curses

from ..keymap import keymap
from .option import option
from ..aart.cursed import aart

#====================================================================

class menu():
	def __init__(self, title="menu", size="fill", coord=(0,0), options=[[]]):
		'''
		Args:
			title (string): title used in ascii art file, or just text to use
			size (tuple) (int,int):
				or "fill" to specify menu to fill the screen
			coord (tuple) (int,int): coordinates in parent screen to place subwindow
			options (2D list of option): arrangement of options
		'''
		self.title = aart(title)
		self.coord = coord
		self.size = size
		self.options = options
		# curses
		self.stdscr = None	# passed from curses.wrapper() #XXX make this static?
		self.window = None # curses.newwin(*size, *coord)

		self.parent = None	# (menu) passed from parent menu
		self.selection = options[0][0]	#XXX select top left be default... should really search for selected
		self.options[0][0].selected=True	#XXX ditto
		self.km=keymap() 				#use a seperate one for menus so people cant lock themselves out of menuing -_-

		# self.__arrange_options()
		self.__link_options()

		self.draw()

	def __repr__(self):
		string = f"\n-------MENU-----------\n"
		string += f"parent:    {self.parent}\n"
		string += f"options:   {self.options}\n"
		string += f"selection: {self.selection}\n"
		string += f"\n-------END-MENU-----------\n"
		return string

	def input(self, key):
		pass
	def __link_options(self):
		# complain if no options
		if len(self.options)==0:
			raise IndexError

		max_r=len(self.options)
		max_c=len(self.options[0])
		# link options to neighbors
		for r in range(max_r):
			for c in range(max_c):
				for direction in self.km.directions:
					dr,dc=self.km.dydx(direction)
					if (r+dr) in range(0,max_r) and (c+dc) in range(0,max_c):	# if neighbor exists
						self.options[r][c].controls[direction] = self.options[r+dr][c+dc] # link to neighbor

	def __arrange_options(self, hug_walls=True):
		'''arrange and link options within bounding box, link to neighbors, and put in parent window
		Args:
			min_coord (tuple): (y,x) coords for upper left
			max_coord (tuple): (y,x) coords for lower right
		'''
		# complain if no options
		if len(self.options)==0:
			raise IndexError

		# arrange title
		self.title.move( (1, (self.size[1]-self.title.size[1])//2) )

		# some tuple ops for int tuples
		tuple_int_op=lambda A,B,op: tuple(op(int(a),int(b)) for a,b in zip(A,B))
		diff=lambda A,B: tuple_int_op(A,B,int.__sub__) # returns A-B where both are tuples
		fdiv=lambda A,B: tuple_int_op(A,B,int.__floordiv__)
		add=lambda A,B: tuple_int_op(A,B,int.__add__)
		mult=lambda A,B: tuple_int_op(A,B,int.__mul__)

		option_dim=(len(self.options), len(self.options[0]))
		title_space=(self.title.size[0], 0)

		availible=diff(self.size, title_space) #(self.size[0]-title_h, self.size[1])
		cell=fdiv(availible, option_dim)
		if min(cell) <=3:
			raise Warning("Screen is to small to house options")

		# arrange coords
		for r in range(option_dim[0]):
			for c in range(option_dim[1]):
				self.options[r][c].arrange(	# send window stuff
					self.window,	
					size=diff(cell, (2,2) ),
					coord=add(add( mult(cell,(r,c)), title_space), (1,1)) # final add shifts down right	#(r*option_size[0],c*option_size[1]) 
					)


	def draw(self):
		'''draws each menu option to screen'''
		if self.stdscr is None:	# no screen to draw to
			return

		self.window.box()
		self.title.draw()	# draw title

		for row in self.options:	# draw options
			for element in row:
				element.draw()

		self.stdscr.refresh()
		self.window.refresh()

	# def draw_title(self):
	# 	self.window.addstr(1,1,self.title.center(self.size[1]-2)) #XXX may get text from file

	def run(self, key):
		'''iterates state based on key input
		'''
		try:
			action=self.selection.controls[self.km(key)]
		except KeyError:	#no action mapped
			return	
		if action is None:
			return
		elif action=="parent":
			self.parent()
			return
		elif isinstance(action, menu): # new menu	# covered by callable()
			action(stdscr=self.stdscr, parent=self)	# pass self as parent, along with back direction?
			return
		elif callable(action):	# function
			action()
			return
		elif isinstance(action, option):	# move selection, update option.selected
			self.selection.toggle()
			self.selection=action
			self.selection.toggle()
			self.draw()
			return
		# elif self.parent is not None:	# has parent, but dont know what to do, panic and go to parent
		# 	self.parent()
		# 	return
		else:
			raise TypeError(f"action of {repr(self.selection)} not recognized")
	def __call__(self, stdscr=None, parent=None):
		if parent is not None:	# don't overwrite parents
			self.parent=parent
		if stdscr is not None:	# dont overwrite
			self.stdscr=stdscr
		if self.stdscr is None:
			raise Warning("Called menu without providing a window to draw to")
		if self.window is None:
			if self.size=="fill":
				diff=lambda A,B:tuple(a-b for a,b in zip(A,B))
				self.size=diff(stdscr.getmaxyx(), self.coord)
			self.window=curses.newwin(*self.size, *self.coord)
			self.__arrange_options()
			self.title.create_window(self.window)

		self.draw()
		key=self.stdscr.getkey()
		while key in "wasdex":
			self.run(key)
			key=self.stdscr.getkey()



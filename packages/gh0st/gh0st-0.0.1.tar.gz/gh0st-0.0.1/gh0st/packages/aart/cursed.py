'''cursed ascii art'''

from pathlib import Path	# for non-relative paths
import curses

from . import aart

class aart(aart):
	def __init__(self, title, filename=Path(__file__).parent/"aart.txt", parent_window=None, coords=(0,0)):
		super().__init__(title, filename)
		self.coords=coords
		self.window=None
		self.parent_window=parent_window
		self.create_window(parent_window)

	@property
	def size(self):
		'''because we cant write to bottom right corner. -_-'''
		return (len(self.strings), self.length+1)

	def draw(self, parent_window=None):
		self.create_window(parent_window)
		if self.window is None:
			raise Warning("called cursed_aart.draw() without providing a window to draw to")
			# return
		for n,line in enumerate(self.strings):
			try:
				self.window.addstr(n,0,line)
			except:
				raise Warning("This is probably writing to the bottom right corner of the window.")


	def create_window(self, parent_window=None):
		if parent_window is not None:
			self.parent_window=parent_window
			self.window=parent_window.derwin(*self.size, *self.coords)

	def move(self, coords):
		self.coords=coords
		self.create_window(self.parent_window)


if __name__=="__main__":
	def main(stdscr):
		title=cursed_aart("gh0st", "aart.txt", stdscr, coords=(10, 20))
		title.draw()
		stdscr.getch()

	curses.wrapper(main)
# from gh0st import main as gh0st
# def main():
# 	gh0st()

'''
Menu system for gh0st
'''

import curses 

from gh0st.packages.menu import menu, option

def play():
	print("You pressed play, sorry there's no game yet")
def credits():
	pass
def quit():
	raise SystemExit
	print("There very well may be no escape\n\nCallback functions anyone?")

play_menu=menu(title="play", size="fill", coord=(0,0), options=[[
	option("Back", action="parent"),
	option("Slot 0"),
	option("Slot 1"),
	option("Slot 2")
	]])

options_menu=menu(title="options", size="fill", coord=(0,0), options=[
	[option("Back", action="parent")],
	[option("A")],
	[option("B")],
	[option("C")],
	[option("D")],
	[option("E")]
	])
main_menu=menu(title="gh0st", size="fill", coord=(0,0), options=[[
		option("Play", action=play_menu),#, selected=True), 
		option("Options", action=options_menu)
	],[
		option("Credits", action=credits), 
		option("Quit", action=quit)
	]])


def main():
	curses.wrapper(main_menu)

if __name__=="__main__":
	main()
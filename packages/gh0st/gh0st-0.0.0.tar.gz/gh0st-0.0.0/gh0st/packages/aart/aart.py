'''ascii art'''
from pathlib import Path	# for non-relative paths
from warnings import warn	# for warning about not finding files or titles within them

class aart():
	'''
	>>> a=aart("gh0st", "aart.txt")
	>>> print(a)
	       _      ____      _
	      | |    / __ \    | |
	  ____| |__ | | /  |___| |_
	 / _' | '_ \| |//| / __| __|
	| |_| | | | |  /_| \__ \ |_
	 \__, |_| |_|\____/|___/\__|
	 /\_/ |
	 \___/
	>>> a.length
	28
	'''
	def __init__(self, title, filename=Path(__file__).parent/"aart.txt"):
		self.title=title
		self.filename=filename
		#set by __read()
		self.strings=[]
		self.length=0

		self.__read()

	@property
	def size(self):
		return (len(self.strings), self.length)
	
	def __str__(self):
		string=""
		for line in self.strings:
			string += line+'\n'
		return string[:-1]
	def __read(self):
		capture=False
		try:
			with open(self.filename, 'r') as file:
				for line in file:
					if line.strip()==self.title:
						if capture:
							break
						capture=True
						continue
					if capture:
						self.strings.append(line[:-1])	# no newlines plz
						self.length = max(self.length, len(line)-1)	# update length
				else:
					warn(f"Title: '{self.title}' was not found in file.")
					self.strings=[self.title]
					self.length=len(self.title)
		except FileNotFoundError:
			warn(f"File: '{self.filename}' does not seem to exist")
			self.strings=[self.title]
			self.length=len(self.title)

if __name__=="__main__":
	a=aart("gh0st", "aart.txt")
	print(a)
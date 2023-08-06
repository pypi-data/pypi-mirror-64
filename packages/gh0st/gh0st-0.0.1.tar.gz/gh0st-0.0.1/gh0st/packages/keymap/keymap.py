class keymap():
	def __init__(self, filename=None):
		self.keyring={
			"up":{"w"},
			"down":{"s"},
			"left":{"a"},
			"right":{"d"},
			"select":{"e"}
		}
		self.filename=filename
		if filename is not None:
			self.read()
		self.directions=('up', 'down', 'left', 'right')

	def __contains__(self, key):
		if self.keyset(key) is not None:
			return True
		return False
	def __str__(self):
		return str(self.keyring)
	__repr__=__str__

	def __call__(self, key):
		for keyset in self.keyring:
			if key in self.keyring[keyset]:
				return keyset
		# raise KeyError
		return None
	# def __neg__(self, )

	def __getitem__(self, keyset):
		if keyset in self.keyring:
			return self.keyring[keyset]

	def __setitem__(self, keyset, value):
		self.keyring[keyset]=value
		self.save()

	def keyset(self, key):
		for keyset in self.keyring:
			if key in self.keyring[keyset]:
				return keyset
		return None
	def inverse(self, keyset):
		'''returns oppisite direction of keyset'''
		lookup={
			"up":"down",
			"down":"up",
			"left":"right",
			"right":"left"
		}
		if keyset in lookup:
			return lookup[keyset]
		return None

	def dydx(self, keyset):
		'''returns tuple of dy, dx for direction'''
		lookup={
			"up":(-1,0),
			"down":(1,0),
			"left":(0,-1),
			"right":(0,1)
		}
		if keyset in lookup:
			return lookup[keyset]
		return None
	def inv(self, key):
		'''returns oppisite direction of key'''
		return self.inverse(self.keyset(key))

	def read(self):	#read from file
		pass
	def save(self):	#save to file
		pass
	def default(self):
		pass
	def clear(self, keyset):
		pass
	def append(self, keyset, key):
		pass
	def remove(self, keyset, key):
		pass
	def replace(self, keyset, rmkey, key):
		self.remove(keyset, rmkey)
		self.append(keyset, key)
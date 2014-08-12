from Manifest import Color, STRIP_LENGTH

class Buffer:
	"""
	Encapsulate a list of Colors.
	@param size Optionally specifies a size for the buffer. By default, it
		is the same size as the LED strip (from the STRIP_LENGTH
		shared constant).
	"""
	def __init__(self, size=STRIP_LENGTH):
		"""
		Initialize a list of default (black) Colors.
		"""
		self._colors = []
		for i in xrange(size):
			self._colors.append(Color())

	def getSize(self):
		return len(self._colors)

	def getColors(self):
		"""
		@return the internal list of Colors, for modification.
		"""
		return self._colors

	def clear(self):
		"""
		Reset all the colors to blank (black).
		"""
		for c in self._colors:
			c.clear()

	def setFromBuffer(self, buffer):
		"""
		Set the contents of this buffer to match another buffer.
		"""
		for localColor, otherColor in zip(
			self._colors, buffer.getColors()):
			localColor.set(otherColor)

	def addBuffer(self, buffer):
		"""
		Add another buffer's colors to this'. Zip from index 0, and do
		not affect or use colors past the end of the shorter buffer.
		"""
		for localColor, otherColor in zip(
			self._colors, buffer.getColors()):
			localColor.add(otherColor)

	def insertAndPop(self, color):
		"""
		Insert the given Color into the beginning (index 0) of the color
		list, and pop a Color from the end (maintaining size).
		"""
		self._colors.insert(0, color)
		return self._colors.pop()


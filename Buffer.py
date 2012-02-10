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
		self.__colors = []
		for i in xrange(size):
			self.__colors.append(Color())

	def getSize(self):
		return len(self.__colors)

	def getColors(self):
		"""
		@return the internal list of Colors, for modification.
		"""
		return self.__colors

	def insertAndPop(self, color):
		"""
		Insert the given Color into the beginning (index 0) of the color
		list, and pop a Color from the end (maintaining size).
		"""
		self.__colors.insert(0, color)
		return self.__colors.pop()


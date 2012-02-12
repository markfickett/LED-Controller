class Pattern:
	"""
	Base class for (animating) color patterns.
	"""
	def __init__(self):
		self.__changed = True
		self.__expired = False

	def apply(self, colorBuffer):
		"""
		Usually, add the colors from the pattern to the given buffer.
		Generally, modify the given color buffer according to this
		pattern's current state.
		"""
		self._clearChanged()

	def isChanged(self):
		"""
		@return whether this Pattern has changed since last rendered.
			Specifically, whether a re-render is necessary on
			account of this Pattern.
		"""
		return self.__changed

	def _setChanged(self):
		self.__changed = True

	def _clearChanged(self):
		self.__changed = False

	def isExpired(self):
		"""
		@return True if calls to apply will never again have an effect
		"""
		return self.__expired

	def _expire(self):
		self.__expired = True


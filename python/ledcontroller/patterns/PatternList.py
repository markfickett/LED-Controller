from Manifest import Pattern

class PatternList(Pattern):
	"""
	Encapsulate management for multiple Patterns: check for changes, apply,
	and discard expired patterns.
	"""
	def __init__(self):
		Pattern.__init__(self)
		self.__patterns = []

	def append(self, pattern):
		"""
		Add the given pattern to the list. Render order matches order of
		addition. Patterns are automatically removed once expired.
		"""
		self.__patterns.append(pattern)

	def remove(self, pattern, strict=True):
		"""
		Remove the given pattern from the list.
		@param strict whether to match the default Python behavior, or
			(if False) to silently do nothing if the pattern is not
			already in the list
		"""
		if strict or (pattern in self.__patterns):
			self.__patterns.remove(pattern)

	def apply(self, colorBuffer):
		for p in self.__patterns:
			p.apply(colorBuffer)

	def isChanged(self):
		"""
		Return whether any pattern in the list has changed. Also do
		garbage collection, removing expired patterns.
		"""
		expired = []
		changed = False
		for p in self.__patterns:
			if p.isExpired():
				expired.append(p)
			else:
				changed |= p.isChanged()
		for p in expired:
			self.__patterns.remove(p)
		return changed


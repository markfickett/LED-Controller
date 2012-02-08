from Manifest import random

class Color:
	BYTE_MAX = 0xFF
	def __init__(self, rgb=None):
		"""
		Create a Color. If no color data is given, the Color
			will be black.
		@param rgb if provided, passed as arguments to setRgb.
		"""
		if rgb:
			self.setRgb(*rgb)
		else:
			self.setRgb(0, 0, 0)

	def setRgb(self, r, g, b):
		"""
		Set from [0.0, 1.0] RGB values.
		"""
		self.__r = float(r)
		self.__g = float(g)
		self.__b = float(b)

	def getRgb(self):
		return [self.__r, self.__g, self.__b]

	def getRgbBytes(self):
		"""
		Get [0x00, 0xFF] RGB values.
		"""
		return [int(min(1, max(0, v)) * self.BYTE_MAX)
			for v in self.getRgb()]

	@classmethod
	def CreateRandom(cls):
		"""
		return new cls(
			random.random(),
			random.random(),
			random.random())	
		"""


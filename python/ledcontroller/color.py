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
			self.SetRgb(*rgb)
		else:
			self.Clear()

	def Clear(self):
		"""
		Reset to the default black color.
		"""
		self.SetRgb(0, 0, 0)

	def SetRgb(self, r, g, b):
		"""
		Set from [0.0, 1.0] RGB values. (Not clamped.)
		"""
		self.__r = float(r)
		self.__g = float(g)
		self.__b = float(b)

	def Set(self, color):
		"""
		Set this Color to match another.
		"""
		self.SetRgb(*color.GetRgb())

	def Clamp(self):
		"""
		Modify this color so that its component values all are within
		expected ranges: RGB in [0.0, 1.0].
		"""
		self.__r, self.__g, self.__b = [
			min(1.0, max(0.0, c)) for c in self.GetRgb()]

	def Add(self, c, clamp=True):
		"""
		Add another color to this one (piecewise RGB).
		@param clamp whether to clamp the Color after the addition
		"""
		self.__r += c.__r
		self.__g += c.__g
		self.__b += c.__b
		if clamp:
			self.Clamp()

	def Scaled(self, f, clamp=True):
		"""
		@param clamp whether to camp the resultant Color before return
		@return a new Color that is this Color with RGB channels
			multiplied by f.
		"""
		c = Color(rgb=[c*f for c in self.GetRgb()])
		if clamp:
			c.Clamp()
		return c

	def GetRgb(self):
		return [self.__r, self.__g, self.__b]

	def GetRgbBytes(self):
		"""
		Get [0x00, 0xFF] RGB values.
		"""
		return [int(min(1, max(0, v)) * self.BYTE_MAX)
			for v in self.GetRgb()]

	@staticmethod
	def Lerp(x, a, b):
		"""
		@return the linear interpolation between Colors a and b,
			where x=0 is a and x=1 is b.
		"""
		lerped = a.Scaled(1.0-x)
		lerped.add(b.Scaled(x))
		return lerped

	@classmethod
	def CreateRandom(cls):
		return cls(rgb=(
			random.random(),
			random.random(),
			random.random()))


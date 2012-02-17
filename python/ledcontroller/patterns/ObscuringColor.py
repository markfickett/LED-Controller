from ledcontroller.Manifest import Color
from Manifest import Pattern

class ObscuringColor(Pattern):
	def __init__(self, color, opacity=0.0):
		Pattern.__init__(self)
		self.__color = color
		self.setOpacity(opacity)

	def setOpacity(self, opacity):
		self._setChanged()
		self.__opacity = opacity

	def apply(self, colorBuffer):
		Pattern.apply(self, colorBuffer)
		for c in colorBuffer.getColors():
			c.set(Color.Lerp(self.__opacity, c, self.__color))


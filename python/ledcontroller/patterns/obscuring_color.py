from ledcontroller.Manifest import Color
from Manifest import Pattern

class ObscuringColor(Pattern):
	def __init__(self, color, opacity=0.0):
		Pattern.__init__(self)
		self.__color = color
		self.SetOpacity(opacity)

	def SetOpacity(self, opacity):
		self._SetChanged()
		self.__opacity = opacity

	def Apply(self, color_buffer):
		Pattern.Apply(self, color_buffer)
		for c in color_buffer.GetColors():
			c.set(Color.Lerp(self.__opacity, c, self.__color))


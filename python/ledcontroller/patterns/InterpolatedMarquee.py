from ledcontroller.Manifest import Buffer, time, STRIP_LENGTH, Color, patterns
from Manifest import Pattern

__all__ = [
	'InterpolatedMarquee',
]

class InterpolatedMarquee(Pattern, Buffer):
	"""
	Manage timed scrolling of a color sequence, and simulate sub-integer
	locations for that movement (sub-pixel smoothing, in effect).
	@param colorSequence an iterable of Color objects, to be scrolled. When
		the colorSequence runs out, the marquee will stop animating.
	@param speed the number of positions (LEDs) to advance in one second.
		For example, with a speed of 5, the first color from
		colorSequence will move (smoothly) from the start of the LED
		strip to the 5th LED.
	Smoothness of animation is dependant on frequency of calls to apply.

	TODO(markfickett) Apparent smoothness also depends on linearity of
	response of the LEDs; that is, how smoothly the perceived luminance
	varies with numeric color value. Nonlinear interpolation may improve
	perceived animation.
	"""
	def __init__(self, colorSequence, speed=1.0):
		if speed <= 0.0:
			raise ValueError('Illegal speed %s must be > 0.'
				% speed)
		Pattern.__init__(self)
		Buffer.__init__(self, size=STRIP_LENGTH + 2)
		self.__seq = iter(colorSequence)
		self.__speed = speed
		self.__offset = 1.0
		self.__t = None

	def isChanged(self):
		return self.__seq is not None

	def setSpeed(self, speed):
		self.__updateColorsAndOffset()
		self.__speed = float(speed)

	def __updateColorsAndOffset(self):
		if self.__seq is None:
			return
		if self.__t is None:
			self.__t = time.time()
		t = time.time()
		self.__offset += (t - self.__t)*self.__speed
		self.__t = t
		while self.__offset >= 1.0:
			try:
				c = self.__seq.next()
			except StopIteration:
				self.__seq = None
				break
			self.insertAndPop(c)
			self.__offset -= 1.0

	def apply(self, colorBuffer):
		Pattern.apply(self, colorBuffer)
		self.__updateColorsAndOffset()
		colors = colorBuffer.getColors()
		f = self.__offset
	 	for i in xrange(min(len(colors), len(self._colors)-1)):
			colors[i].add(self._colors[i].scaled(f))
			colors[i].add(self._colors[i+1].scaled(1.0-f))


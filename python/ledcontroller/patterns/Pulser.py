from Manifest import Pattern
from ledcontroller.Manifest import Buffer, Color, time

class Pulser(Pattern):
	"""
	Send pulses of a color along the LED strip.
	@param color the color of the center (maximally intense part) of a pulse
	@param width the maximum number of LEDs affected by a pulse (diameter)
	@param addDelay the number of seconds between new pulses
	@param speed the number of LEDs down the strip a pulse travels / second
	@param reverse If True, pulses travel in the opposite direction; by
		default, the start from index 0.
	"""
	def __init__(self, addDelay=1.0, speed=14.0,
			color=Color(rgb=(1,1,1)), width=6.0,
			reverse=False):
		Pattern.__init__(self)
		if addDelay <= 0:
			raise ValueError('addDelay value %s is not > 0.'
				% addDelay)
		if speed == 0:
			raise ValueError('speed value %s is 0.')
		if width <= 0:
			raise ValueError('width value %s is not > 0.'
				% width)
		self.__addDelay = float(addDelay)
		self.__speed = float(speed)
		self.__interval = self.__speed * self.__addDelay
		self.__radius = width/2.0
		self.__reverse = reverse
		self.__color = color

		self.__t0 = None

	def isChanged(self):
		return True

	def __generatePositions(self, maxIndex):
		t = time.time()
		if self.__t0 is None:
			self.__t0 = t
		dt = t - self.__t0
		maxPos = maxIndex + self.__radius
		repeats = int(dt / self.__addDelay)
		dt -= repeats*self.__addDelay
		i = 0
		p = -self.__radius + self.__speed*dt
		while i <= repeats and p <= maxPos:
			yield p
			p += self.__interval
			i += 1

	def apply(self, colorBuffer):
		"""
		Recalculate pulse positions for the current time and add pulses.
		"""
		Pattern.apply(self, colorBuffer)
		colors = colorBuffer.getColors()
		n = len(colors)
		for rawCenter in self.__generatePositions(n-1):
			center = rawCenter
			if self.__reverse:
				center = (n - 1) - center
			minIndex = int(1 + center - self.__radius)
			maxIndex = int(center + self.__radius)
			for i in xrange(minIndex, maxIndex+1):
				if i < 0 or i >= n:
					continue
				dx = abs(center - i)
				f = min(1.0, dx / self.__radius)
				colors[i] = colors[i].scaled(f)
				colors[i].add(self.__color.scaled(1.0 - f))

